"""Classe utilizzata per implementare tecniche di selezione delle feature."""
from cefeste import FeatureAnalysis
from cefeste.utils import remove_features, get_numerical_features, convert_Int_series
from cefeste.selection.explanatory import find_not_explanatory
from cefeste.selection.multivariate import find_collinear_feature_optimized, find_correlated_features
from cefeste.selection.univariate import (
    find_constant_features,
    find_high_topcat_features,
    find_low_nvalues_features,
    find_missing_features,
    find_unstable_psi_features,
)

import warnings
from itertools import combinations
from functools import reduce

import pandas as pd
from numpy import nan


class FeatureSelection(FeatureAnalysis):
    """Classe utilizzata per implementare tecniche di selezione delle feature.

    Questa classe estende la classe `FeatureAnalysis` per fornire una pipeline configurabile per la selezione delle feature. Applica una serie di filtri univariati e multivariati per identificare e rimuovere le feature che non rispettano vari criteri di selezione.

    Filtri Applicati:
        - **Constant Features**:
            Identifica e rimuove le feature che presentano un unico valore costante in tutto il dataset (o nel set di training). Parametri rilevanti: Nessuno specifico, agisce sulla natura della feature.

        - **Missing Features**:
            Identifica e rimuove le feature che superano una soglia definita di valori mancanti. Parametri rilevanti: `max_pct_missing` (default 0.9).

        - **Highly Concentrated Features**:
            Identifica e rimuove le feature in cui un singolo valore (il più frequente) supera una certa percentuale del totale delle osservazioni. Parametri rilevanti: `max_pct_mfv` (default 0.95).

        - **Low Values Features**:
            Identifica e rimuove le feature che hanno un numero di valori unici inferiore a una soglia specificata. Utile per rimuovere feature quasi costanti o con cardinalità troppo bassa per essere informative. Parametri rilevanti: `min_unique_val` (default 3).

        - **Unstable Features (PSI)**:
            Identifica e rimuove le feature la cui distribuzione cambia significativamente tra diversi campioni di dati (es. training vs. test, o periodi temporali diversi), utilizzando il Population Stability Index (PSI). Richiede la definizione di `sample_col`. Parametri rilevanti: `max_psi` (default 0.2), `psi_nbins` (default 20), `psi_bin_min_pct` (default 0.02).

        - **Unexplanatory Features**:
            Identifica e rimuove le feature che mostrano un basso potere esplicativo nei confronti della variabile target. La metrica di valutazione dipende da `algo_type` (AUC per classificazione, R-squared per regressione). Richiede la definizione di `target_col`. Parametri rilevanti: `explanatory_threshold` (default 0.05), `algo_type` (default "auto"), `dim_cat_threshold` (default 10).

        - **Correlated Features**:
            Identifica e rimuove le feature che sono altamente correlate con altre feature. Tra una coppia di feature correlate, una viene rimossa in base a `selection_rule` (es. casualmente, o quella con potere esplicativo sul target minore). Parametri rilevanti: `correlation_threshold` (default 0.95), `selection_rule` (default "random"), `random_state` (default 42).

        - **Collinear Features (VIF)**:
            Identifica e rimuove le feature numeriche che sono linearmente dipendenti da altre feature numeriche, utilizzando il Variance Inflation Factor (VIF). Aiuta a mitigare problemi di multicollinearità. Parametri rilevanti: `vif_threshold` (default 5), `collinear_optimize` (default `False`).


    La classe tiene traccia delle feature rimosse e del motivo della rimozione, fornendo report dettagliati.
    """

    def __init__(
        self,
        # DB / Feature Parameters
        db,
        feat_to_check=None,
        target_col=None,
        algo_type="auto",
        sample_col=None,
        sample_train_value=None,
        # Univariate Analysis Parameters
        min_unique_val=3,
        max_pct_missing=0.9,
        max_pct_mfv=0.95,
        max_psi=0.2,
        psi_nbins=20,
        psi_bin_min_pct=0.02,
        # Univariate Explanatory Power Parameters
        explanatory_threshold=0.05,
        # Multivariate Analysis Parameters
        correlation_threshold=0.95,
        selection_rule="random",
        vif_threshold=5,
        collinear_optimize=False,
        return_selection_history=True,
        dim_cat_threshold=10,
        # Generic Parameters
        random_state=42,
        verbose=True,
    ):
        """Inizializza l'oggetto FeatureSelection con dati e parametri di configurazione.

        Questo costruttore imposta il `DataFrame` da analizzare, le feature da considerare, la colonna target (se presente), la colonna per la suddivisione in campioni (es. train/test), il tipo di algoritmo di machine learning (per guidare alcune selezioni) e varie soglie e parametri per i diversi passaggi di filtraggio delle feature. Inizializza anche attributi interni per memorizzare i risultati di ogni fase di selezione e lo stato generale.

        Args:
            db (`pd.DataFrame`): `DataFrame` da analizzare.
            feat_to_check (`list`, optional): Lista delle feature da analizzare. Se `None`, vengono utilizzate tutte le colonne tranne `target_col` e `sample_col`. Default: `None`.
            target_col (`str`, optional): Nome della colonna target. Necessario per i filtri basati sul potere esplicativo. Default: `None`.
            algo_type (`str`, optional): Tipo di algoritmo di machine learning. Può essere 'auto', 'regression', 'classification', 'multiclass', 'unsupervised'. Se 'auto' e `target_col` è specificato, il tipo viene calcolato in base al numero di valori unici del target. Default: "auto".
            sample_col (`str`, optional): Nome della colonna che indica se i campioni appartengono a 'train' o 'test'. Usato per l'analisi di stabilità (PSI) e per applicare alcuni filtri solo sul campione di training. Default: `None`.
            sample_train_value (`str`, optional): Valore nella `sample_col` che identifica il set di training. Necessario se `sample_col` è specificato e si desidera applicare filtri specifici al training set. Default: `None`.
            min_unique_val (`int`, optional): Numero minimo di valori unici che una feature deve avere per non essere considerata "low_values". Default: 3.
            max_pct_missing (`float`, optional): Percentuale massima di valori mancanti tollerata in una feature. Default: 0.9.
            max_pct_mfv (`float`, optional): Percentuale massima della frequenza tollerata dei valori di una feature. Default: 0.95.
            max_psi (`float`, optional): Valore massimo di Population Stability Index (PSI) tollerato tra le distribuzioni del training con il test. Default: 0.2.
            psi_nbins (`int`, optional): Numero di bin da utilizzare per il calcolo del PSI. Default: 20.
            psi_bin_min_pct (`float`, optional): Percentuale minima di osservazioni per bin nel calcolo del PSI. Default: 0.02.
            explanatory_threshold (`float`, optional): Soglia per il potere esplicativo. Feature con performance (es. AUC, R-squared) inferiori a questa soglia rispetto al target vengono rimosse. Default: 0.05.
            correlation_threshold (`float`, optional): Soglia di correlazione. Feature con correlazione (assoluta) superiore a questa soglia vengono considerate per la rimozione. Default: 0.95.
            selection_rule (`str`, optional): Regola per decidere quale feature rimuovere tra una coppia di feature altamente correlate. Può essere 'random' o 'univ_perf', ovvero basata sul potere esplicativo rispetto alla variabile target. Default: "random".
            vif_threshold (`int`, optional): Soglia per il Variance Inflation Factor (VIF). Feature numeriche con VIF superiore a questa soglia vengono considerate per la rimozione a causa della multicollinearità. Default: 5.
            collinear_optimize (`bool`, optional): Se `True`, tenta di ottimizzare la rimozione delle feature collineari basandosi sulla loro correlazione media o potere esplicativo rispetto alla variabile target. Default: False.
            return_selection_history (`bool`, optional): Se `True`, memorizza e restituisce la storia dettagliata della selezione delle feature correlate. Default: True.
            dim_cat_threshold (`int`, optional): Soglia di cardinalità per le feature categoriche. Se una feature categorica ha più valori unici di questa soglia, solo le top `dim_cat_threshold` categorie più frequenti vengono codificate con One-Hot Encoding (le altre vengono ignorate). Se `None`, viene applicato One-Hot Encoding standard a tutte le categorie. Default: 10.
            verbose (`bool`, optional): Se `True`, stampa informazioni aggiuntive durante l'esecuzione dei filtri. Default: `True`.

        Note:
            Se `algo_type` è ‘auto’ per l’approccio supervisionato, questo verrà determinato in base al numero di valori unici nel target:

                <=2 -> 'classification' (Classificazione Binaria)

                <11 -> 'multiclass' (Classificazione Multiclasse)

                >=11 -> 'regression' (Regressione)
        """
        super().__init__(db, feat_to_check)
        self.feat_to_check = list(set(self.feat_to_check) - set([target_col, sample_col]))
        # Target check
        if (target_col in db.columns) | (target_col is None):
            self.target_col = target_col
        else:
            raise ValueError(f"{target_col} not in DataFrame")

        # Check the target var and set the algo type
        if algo_type not in ["auto", "regression", "classification", "multiclass", "unsupervised"]:
            raise ValueError(
                f"{algo_type} is not a valid algo_type. It should be one of the following:\n ['auto', 'regression', 'classification', 'multiclass', 'unsupervised']"
            )

        if target_col is not None:
            vals = db[target_col].nunique()
            if vals == 1:
                raise ValueError(f"The target column {target_col} selected is constant")
            elif algo_type != "auto":
                self.algo_type = algo_type
            elif vals == 2:
                self.algo_type = "classification"
            elif vals < 11:
                self.algo_type = "multiclass"
            else:
                self.algo_type = "regression"
        else:
            self.algo_type = "unsupervised"

        # Sample column check
        if (sample_col in db.columns) | (sample_col is None):
            self.sample_col = sample_col
        else:
            raise ValueError(f"{sample_col} not in DataFrame")
        # Save the list of samples in db
        if sample_col is not None:
            self._sample_list = db[sample_col].unique()
            self._n_sample = db[sample_col].nunique()
        else:
            self._sample_list = []
            self._n_sample = 0
        # Sample Train value
        if (sample_train_value is not None) & (sample_train_value not in self._sample_list):
            raise ValueError(
                f"The value {sample_train_value} set for parameter sample_train_value is not in {sample_col}."
            )
        else:
            self.sample_train_value = sample_train_value

        # Parameters
        self.min_unique_val = min_unique_val
        self.max_pct_missing = max_pct_missing
        self.max_pct_mfv = max_pct_mfv
        self.max_psi = max_psi
        self.psi_nbins = psi_nbins
        self.psi_bin_min_pct = psi_bin_min_pct
        self.explanatory_threshold = explanatory_threshold
        self.correlation_threshold = correlation_threshold
        self.selection_rule = selection_rule
        self.vif_threshold = vif_threshold
        self.collinear_optimize = collinear_optimize
        self.random_state = random_state
        self.verbose = verbose
        self.return_selection_history = return_selection_history
        self.dim_cat_threshold = dim_cat_threshold

        # Initialize the attributes as empty lists/dataframes
        self._constant_features = []
        self._missing_features = []
        self._highly_concentrated_features = []
        self._low_values_features = []
        self._unstable_features = []
        self._unexplanatory_features = []
        self._correlated_features = []
        self._collinear_features = []
        self._selected_features = self.feat_to_check
        self._filtered_out_features = []
        self._funnel_df = pd.DataFrame(
            {
                "Step_Description": "Initial feat to check",
                "Col_Removed": 0,
                "Col_Kept": len(self.feat_to_check),
                "Params": nan,
            },
            index=[0],
        ).rename_axis("Step_Number")

        # Initialize the attributes as False
        self.filter_constant = False
        self.filter_missing = False
        self.filter_missing = False
        self.filter_highly_concentrated = False
        self.filter_low_values = False
        self.filter_unstable = False
        self.filter_unexplanatory = False
        self.filter_correlated = False
        self.filter_collinear = False

        self._perf_db = pd.DataFrame()
        self._selection_history = pd.DataFrame()

    def run(
        self,
        filter_constant=True,
        filter_missing=True,
        filter_highly_concentrated=True,
        filter_low_values=False,
        filter_unstable=True,
        filter_unexplanatory=True,
        filter_correlated=True,
        filter_collinear=True,
        **kwargs,
    ):
        """Esegue la pipeline di selezione delle feature in base ai filtri e ai parametri configurati.

        Questo è il metodo principale per eseguire il processo di selezione. Applica in sequenza i vari filtri (costanti, mancanti, concentrati, ecc.) alle feature specificate. Per ogni filtro attivo, identifica le feature da rimuovere, aggiorna lo stato interno dell'oggetto e riduce il set di feature considerate per i passaggi successivi. I filtri vengono applicati principalmente sul training set se `sample_col` e `sample_train_value` sono specificati, altrimenti sull'intero dataset.

        Args:
            filter_constant (`bool`, optional): Se `True`, attiva il filtro per le feature costanti. Default: `True`. (Per dettagli vedere :meth:`~cefeste.selection.FeatureSelection.find_constant_features`)
            filter_missing (`bool`, optional): Se `True`, attiva il filtro per le feature con troppi valori mancanti. Default: `True`. (Per dettagli vedere :meth:`~cefeste.selection.FeatureSelection.find_missing_features`)
            filter_highly_concentrated (`bool`, optional): Se `True`, attiva il filtro per le feature altamente concentrate. Default: `True`. (Per dettagli vedere :meth:`~cefeste.selection.FeatureSelection.find_high_topcat_features`)
            filter_low_values (`bool`, optional): Se `True`, attiva il filtro per le feature con pochi valori unici. Default: `False`. (Per dettagli vedere :meth:`~cefeste.selection.FeatureSelection.find_low_nvalues_features`)
            filter_unstable (`bool`, optional): Se `True`, attiva il filtro per le feature instabili tra campioni (basato su PSI). Richiede `sample_col`. Default: `True`. (Per dettagli vedere :meth:`~cefeste.selection.FeatureSelection.find_unstable_psi_features`)
            filter_unexplanatory (`bool`, optional): Se `True`, attiva il filtro per le feature non esplicative rispetto al target. Richiede `target_col`. Default: `True`. (Per dettagli vedere :meth:`~cefeste.selection.FeatureSelection.find_not_explanatory`)
            filter_correlated (`bool`, optional): Se `True`, attiva il filtro per le feature altamente correlate. Default: `True`. (Per dettagli vedere :meth:`~cefeste.selection.FeatureSelection.find_correlated_features`)
            filter_collinear (`bool`, optional): Se `True`, attiva il filtro per le feature collineari (basato su VIF). Default: `True`. (Per dettagli vedere :meth:`~cefeste.selection.FeatureSelection.find_collinear_feature_optimized`)
            **kwargs: Argomenti keyword aggiuntivi che possono essere usati per sovrascrivere i parametri dei singoli filtri prima dell'esecuzione (es. `max_pct_missing=0.8`).

        Note:
            - L'ordine di applicazione dei filtri è predefinito e può influenzare quali feature vengono rimosse da quale criterio se una feature soddisfa più criteri di rimozione.
            - I risultati, come le feature selezionate e i report, sono memorizzati negli attributi dell'istanza.
            - Per vedere quali parametri si possono inserire nei kwargs guardare dettagli in ogni filtro.
            - Gli attributi principali che vengono modificati per ogni filtro sono `_selected_features` e `_filtered_out_features`, rispettivamente le feature considerate "buone" e quelle che vengono eliminate dai filtri.

        **Dati utilizzati per gli esempi:**

        >>> df_test_filters

        .. raw:: html

            <style>
                   /* Stile base per la tabella con la nostra classe specifica */
                   .jupyter-style-table {
                       border-collapse: collapse; /* Bordi uniti */
                       margin: 1em 0; /* Margine sopra/sotto */
                       font-family: "Helvetica Neue", Helvetica, Arial, sans-serif; /* Font simile a Jupyter */
                       font-size: 0.9em; /* Dimensione font leggermente ridotta */
                       border: 1px solid #d3d3d3; /* Bordo esterno leggero */
                       width: auto; /* Larghezza basata sul contenuto */
                       max-width: 100%; /* Non superare il contenitore */
                       overflow-x: auto; /* Abilita lo scroll orizzontale se necessario (meglio sul wrapper, ma ok qui) */
                       display: block; /* Necessario per far funzionare overflow-x su una tabella */
                   }

                   /* Stile per le celle dell'header (th) */
                   .jupyter-style-table thead th {
                       background-color: #f5f5f5; /* Sfondo grigio chiaro per header */
                       font-weight: bold; /* Grassetto */
                       padding: 8px 10px; /* Padding interno */
                       text-align: right; /* Allineamento testo (spesso a destra per numeri/default) */
                       border-bottom: 1px solid #d3d3d3; /* Linea sotto l'header */
                       vertical-align: bottom; /* Allineamento verticale */
                   }

                   /* Stile per le celle dei dati (td) */
                   .jupyter-style-table tbody td {
                       padding: 6px 10px; /* Padding interno */
                       text-align: right; /* Allineamento testo (aggiusta se hai testo a sinistra) */
                       border-right: 1px solid #d3d3d3; /* Linea verticale tra celle (opzionale) */
                       border-top: 1px solid #d3d3d3; /* Linea orizzontale tra righe */
                       vertical-align: middle; /* Allineamento verticale */
                   }
                   .jupyter-style-table tbody td:last-child {
                       border-right: none; /* Rimuovi bordo destro sull'ultima cella */
                   }

                   /* Stile per l'header dell'indice (se presente) */
                   .jupyter-style-table thead th.blank { /* Header vuoto sopra l'indice */
                       background-color: white;
                       border: none;
                   }
                   .jupyter-style-table tbody th { /* Celle dell'indice nel body */
                       padding: 6px 10px;
                       text-align: right;
                       font-weight: normal;
                       border-right: 1px solid #d3d3d3;
                       border-top: 1px solid #d3d3d3;
                       background-color: #f5f5f5; /* Sfondo leggero per indice */
                   }


                   /* Striping delle righe (alternanza colori) */
                   .jupyter-style-table tbody tr:nth-child(even) {
                       background-color: #f9f9f9; /* Sfondo molto leggero per righe pari */
                   }

                   /* Effetto Hover (cambio colore al passaggio del mouse) */
                   .jupyter-style-table tbody tr:hover {
                       background-color: #f0f0f0; /* Sfondo leggermente più scuro su hover */
                   }
                </style>
                <table border="0" class="jupyter-style-table">  <thead>    <tr style="text-align: right;">      <th></th>      <th>feature_B</th>      <th>feature_C</th>      <th>target</th>      <th>feature_A1</th>      <th>feature_A2</th>      <th>sample_col</th>    </tr>  </thead>  <tbody>    <tr>      <th>0</th>      <td>34.835708</td>      <td>Z</td>      <td>75.013312</td>      <td>-0.270712</td>      <td>-0.812137</td>      <td>train</td>    </tr>    <tr>      <th>1</th>      <td>3.086785</td>      <td>X</td>      <td>109.194174</td>      <td>0.104848</td>      <td>0.314544</td>      <td>train</td>    </tr>    <tr>      <th>2</th>      <td>42.384427</td>      <td>Y</td>      <td>96.287048</td>      <td>0.250528</td>      <td>0.751583</td>      <td>train</td>    </tr>    <tr>      <th>3</th>      <td>86.151493</td>      <td>X</td>      <td>264.905765</td>      <td>-0.925200</td>      <td>-2.775600</td>      <td>train</td>    </tr>    <tr>      <th>4</th>      <td>-1.707669</td>      <td>V</td>      <td>2.880829</td>      <td>0.567144</td>      <td>1.701431</td>      <td>train</td>    </tr>    <tr>      <th>5</th>      <td>-1.706848</td>      <td>V</td>      <td>2.318509</td>      <td>-1.040180</td>      <td>-3.120541</td>      <td>train</td>    </tr>    <tr>      <th>6</th>      <td>88.960641</td>      <td>X</td>      <td>273.054387</td>      <td>-0.153676</td>      <td>-0.461028</td>      <td>train</td>    </tr>    <tr>      <th>7</th>      <td>48.371736</td>      <td>V</td>      <td>101.779140</td>      <td>0.789852</td>      <td>2.369555</td>      <td>train</td>    </tr>    <tr>      <th>8</th>      <td>-13.473719</td>      <td>Z</td>      <td>-25.266714</td>      <td>-1.226216</td>      <td>-3.678648</td>      <td>train</td>    </tr>    <tr>      <th>9</th>      <td>37.128002</td>      <td>Y</td>      <td>73.118623</td>      <td>-0.948007</td>      <td>-2.844021</td>      <td>train</td>    </tr>    <tr>      <th>10</th>      <td>-13.170885</td>      <td>X</td>      <td>69.538553</td>      <td>-0.569654</td>      <td>-1.708962</td>      <td>train</td>    </tr>    <tr>      <th>11</th>      <td>-13.286488</td>      <td>Z</td>      <td>-30.168523</td>      <td>-0.977150</td>      <td>-2.931451</td>      <td>train</td>    </tr>    <tr>      <th>12</th>      <td>22.098114</td>      <td>W</td>      <td>54.445288</td>      <td>-0.770632</td>      <td>-2.311895</td>      <td>train</td>    </tr>    <tr>      <th>13</th>      <td>-85.664012</td>      <td>W</td>      <td>-171.324610</td>      <td>-0.033711</td>      <td>-0.101134</td>      <td>train</td>    </tr>    <tr>      <th>14</th>      <td>-76.245892</td>      <td>X</td>      <td>-48.581133</td>      <td>-1.032859</td>      <td>-3.098578</td>      <td>train</td>    </tr>    <tr>      <th>15</th>      <td>-18.114376</td>      <td>X</td>      <td>59.816750</td>      <td>1.142427</td>      <td>3.427282</td>      <td>train</td>    </tr>    <tr>      <th>16</th>      <td>-40.641556</td>      <td>Z</td>      <td>-85.182377</td>      <td>-0.609778</td>      <td>-1.829334</td>      <td>train</td>    </tr>    <tr>      <th>17</th>      <td>25.712367</td>      <td>Y</td>      <td>56.834657</td>      <td>1.469416</td>      <td>4.408249</td>      <td>train</td>    </tr>    <tr>      <th>18</th>      <td>-35.401204</td>      <td>Y</td>      <td>-77.550289</td>      <td>1.492679</td>      <td>4.478037</td>      <td>train</td>    </tr>    <tr>      <th>19</th>      <td>-60.615185</td>      <td>Y</td>      <td>-123.306439</td>      <td>0.707125</td>      <td>2.121376</td>      <td>train</td>    </tr>  </tbody></table>

        **Esempio:**

        >>> from cefeste.selection import FeatureSelection
        >>> fs = FeatureSelection(
        ...  db=df_test_filters,
        ...  target_col='target',
        ...  sample_col='sample_col',
        ...  sample_train_value='train',
        ...  verbose=True
        ... )
        >>> fs.run()
        >>> fs.make_report()

        .. raw:: html

            <table border="0" class="jupyter-style-table">  <thead>    <tr style="text-align: right;">      <th></th>      <th>feat_name</th>      <th>result</th>      <th>drop_reason</th>    </tr>  </thead>  <tbody>    <tr>      <th>0</th>      <td>feature_A1</td>      <td>drop</td>      <td>unexplanatory</td>    </tr>    <tr>      <th>1</th>      <td>feature_A2</td>      <td>drop</td>      <td>unexplanatory</td>    </tr>    <tr>      <th>2</th>      <td>feature_C</td>      <td>keep</td>      <td>NaN</td>    </tr>    <tr>      <th>3</th>      <td>feature_B</td>      <td>keep</td>      <td>NaN</td>    </tr>  </tbody></table>
        """
        self.set_params(exceptions="feat_to_check", **kwargs)
        # for k, v in kwargs.items():
        #    self.__dict__[k] = v

        db = self.db
        db.reset_index(inplace=True, drop=True)

        if self.sample_col is not None:
            df, sample_series = self.db.drop(columns=self.sample_col), self.db[self.sample_col]
        else:
            df = db

        if self.target_col is not None:
            X, y = df.drop(columns=self.target_col), df[self.target_col]
        else:
            X = df
        X = X[self._selected_features]
        # self._X_original = X

        if self.sample_train_value is not None:
            X_train = X.loc[sample_series == self.sample_train_value]
        else:
            X_train = X

        if filter_constant:
            _constant_features = find_constant_features(
                X_train,
            )
            self.__union__("_constant_features", _constant_features)
            self._funnel_df.loc[self._funnel_df.shape[0]] = pd.Series(
                {
                    "Step_Description": "Constant",
                    "Col_Removed": len(_constant_features),
                    "Col_Kept": len(X_train.columns) - len(_constant_features),
                    "Params": nan,
                }
            )
            X_train = remove_features(X_train, _constant_features)

        if filter_missing:
            _missing_features = find_missing_features(
                X_train,
            )
            self.__union__("_missing_features", _missing_features)
            self._funnel_df.loc[self._funnel_df.shape[0]] = pd.Series(
                {
                    "Step_Description": "Missing",
                    "Col_Removed": len(_missing_features),
                    "Col_Kept": len(X_train.columns) - len(_missing_features),
                    "Params": {"max_pct_missing": self.max_pct_missing},
                }
            )
            X_train = remove_features(X_train, _missing_features)

        if filter_highly_concentrated:
            _highly_concentrated_features = find_high_topcat_features(X_train, max_pct_mfv=self.max_pct_mfv)
            self.__union__("_highly_concentrated_features", _highly_concentrated_features)
            self._funnel_df.loc[self._funnel_df.shape[0]] = pd.Series(
                {
                    "Step_Description": "Highly Concentrated",
                    "Col_Removed": len(_highly_concentrated_features),
                    "Col_Kept": len(X_train.columns) - len(_highly_concentrated_features),
                    "Params": {"max_pct_mfv": self.max_pct_mfv},
                }
            )
            X_train = remove_features(X_train, _highly_concentrated_features)

        if filter_low_values:
            _low_values_features = find_low_nvalues_features(X_train, min_unique_val=self.min_unique_val)
            self.__union__("_low_values_features", _low_values_features)
            self._funnel_df.loc[self._funnel_df.shape[0]] = pd.Series(
                {
                    "Step_Description": "Low Values",
                    "Col_Removed": len(_low_values_features),
                    "Col_Kept": len(X_train.columns) - len(_low_values_features),
                    "Params": {"min_unique_val": self.min_unique_val},
                }
            )
            X_train = remove_features(X_train, _low_values_features)

        X = X[X_train.columns]

        if filter_unstable:
            if self.sample_col is None:
                filter_unstable = False
                warnings.warn("filter unstable not performed since no sample columns defined")
            elif self._n_sample <= 1:
                filter_unstable = False
                warnings.warn("filter unstable not performed since sample columns defined is constant")
            else:
                sample_comb = list(combinations(self._sample_list, 2))
                unstable_dict = {}
                for comb in sample_comb:
                    if (self.sample_train_value in comb) | (self.sample_train_value is None):
                        base = X.loc[sample_series == comb[0]]
                        compare = X.loc[sample_series == comb[1]]
                        unstable_dict[comb] = find_unstable_psi_features(
                            # evetually add a parameter to specify wich combination we are currenty considering
                            base,
                            compare,
                            max_psi=self.max_psi,
                            psi_bin_min_pct=self.psi_bin_min_pct,
                            psi_nbins=self.psi_nbins,
                        )

                _unstable_features = list(reduce(lambda x, y: set(x) | set(y), unstable_dict.values()))
                self.__union__("_unstable_features", _unstable_features)
                self._funnel_df.loc[self._funnel_df.shape[0]] = pd.Series(
                    {
                        "Step_Description": "Unstable",
                        "Col_Removed": len(_unstable_features),
                        "Col_Kept": len(X_train.columns) - len(_unstable_features),
                        "Params": {
                            "max_psi": self.max_psi,
                            "psi_bin_min_pct": self.psi_bin_min_pct,
                            "psi_nbins": self.psi_nbins,
                        },
                    }
                )
                X = remove_features(X, _unstable_features)

        if filter_unexplanatory:
            if self.target_col is None:
                filter_unexplanatory = False
                warnings.warn("filter unexplanatory not performed since no target columns defined")
            elif (self.sample_col is None) | (self._n_sample <= 1):
                warnings.warn("filter unexplanatory considering the whole dataset belonging to the same split")
                _unexplanatory_features, _perf_db = find_not_explanatory(
                    X,
                    None,
                    convert_Int_series(y),
                    None,
                    threshold=self.explanatory_threshold,
                    algo_type=self.algo_type,
                    dim_cat_threshold=self.dim_cat_threshold,
                )
                self._perf_db = _perf_db
                self.__union__("_unexplanatory_features", _unexplanatory_features)
                self._funnel_df.loc[self._funnel_df.shape[0]] = pd.Series(
                    {
                        "Step_Description": "Unexplanatory",
                        "Col_Removed": len(_unexplanatory_features),
                        "Col_Kept": len(X.columns) - len(_unexplanatory_features),
                        "Params": {
                            "threshold": self.explanatory_threshold,
                            "algo_type": self.algo_type,
                            "dim_cat_threshold": self.dim_cat_threshold,
                        },
                    }
                )
                X = remove_features(X, _unexplanatory_features)
            else:
                sample_comb = list(combinations(self._sample_list, 2))
                unexpl_dict = {}
                perf_dict = {}
                for comb in sample_comb:
                    if (self.sample_train_value in comb) | (self.sample_train_value is None):
                        baseX = X.loc[sample_series == comb[0]]
                        compareX = X.loc[sample_series == comb[1]]
                        basey = y.loc[sample_series == comb[0]]
                        comparey = y.loc[sample_series == comb[1]]
                        unexpl_dict[comb], _perf_ = find_not_explanatory(
                            baseX,
                            compareX,
                            convert_Int_series(basey),
                            convert_Int_series(comparey),
                            threshold=self.explanatory_threshold,
                            algo_type=self.algo_type,
                            dim_cat_threshold=self.dim_cat_threshold,
                        )
                        perf_dict[comb] = _perf_[["name", "perf"]].copy()

                _unexplanatory_features = list(reduce(lambda x, y: set(x) | set(y), unexpl_dict.values()))
                perf_db = reduce(
                    lambda x, y: x.merge(y, left_index=True, right_index=True, how="outer"), perf_dict.values()
                )
                perf_db.set_index("name", inplace=True)
                perf_db["perf"] = perf_db.min(axis=1)
                _perf_db = perf_db[["perf"]].reset_index()
                self._perf_db = _perf_db
                self.__union__("_unexplanatory_features", _unexplanatory_features)
                self._funnel_df.loc[self._funnel_df.shape[0]] = pd.Series(
                    {
                        "Step_Description": "Unexplanatory",
                        "Col_Removed": len(_unexplanatory_features),
                        "Col_Kept": len(X.columns) - len(_unexplanatory_features),
                        "Params": {
                            "threshold": self.explanatory_threshold,
                            "algo_type": self.algo_type,
                            "dim_cat_threshold": self.dim_cat_threshold,
                        },
                    }
                )
                X = remove_features(X, _unexplanatory_features)

        X_train = X_train[X.columns]

        if (filter_correlated) & (X_train.shape[1] > 1):
            _correlated_features, selection_history, self._avg_corr = find_correlated_features(
                X_train,
                correlation_threshold=self.correlation_threshold,
                selection_rule=self.selection_rule,
                random_state=self.random_state,
                feat_univ_perf=self._perf_db,
                return_selection_history=self.return_selection_history,
                verbose=self.verbose,
                return_avg_corr=True,
            )
            if self.return_selection_history:
                self._selection_history = pd.concat([self._selection_history, selection_history])
            self.__union__("_correlated_features", _correlated_features)
            self._funnel_df.loc[self._funnel_df.shape[0]] = pd.Series(
                {
                    "Step_Description": "Correlated",
                    "Col_Removed": len(_correlated_features),
                    "Col_Kept": len(X_train.columns) - len(_correlated_features),
                    "Params": {
                        "correlation_threshold": self.correlation_threshold,
                        "selection_rule": self.selection_rule,
                        "random_state": self.random_state,
                    },
                }
            )
            X_train = remove_features(X_train, _correlated_features)

        if (filter_collinear) & (len(get_numerical_features(X_train)) > 1):
            if (not self.collinear_optimize) | (not (filter_correlated or filter_unexplanatory)):
                self.collinear_optimize = False
                optim_Series = None
                optim_value_ascending = True

            elif filter_correlated:
                optim_Series = self._avg_corr
                optim_value_ascending = False
            else:
                optim_Series = self._perf_db.set_index("name")["perf"]
                optim_value_ascending = True

            _collinear_features = find_collinear_feature_optimized(
                X_train,
                vif_threshold=self.vif_threshold,
                verbose=self.verbose,
                optimize=self.collinear_optimize,
                optim_Series=optim_Series,
                optim_value_ascending=optim_value_ascending,
            )
            self.__union__("_collinear_features", _collinear_features)
            self._funnel_df.loc[self._funnel_df.shape[0]] = pd.Series(
                {
                    "Step_Description": "Collinear",
                    "Col_Removed": len(_collinear_features),
                    "Col_Kept": len(X_train.columns) - len(_collinear_features),
                    "Params": {
                        "vif_threshold": self.vif_threshold,
                        "optimize": self.collinear_optimize,
                        # I did not put optim_value_ascending cause it is decided automatically
                    },
                }
            )
            X_train = remove_features(X_train, _collinear_features)

        self.filter_constant |= filter_constant
        self.filter_missing |= filter_missing
        self.filter_highly_concentrated |= filter_highly_concentrated
        self.filter_low_values |= filter_low_values
        self.filter_unstable |= filter_unstable
        self.filter_unexplanatory |= filter_unexplanatory
        self.filter_correlated |= filter_correlated
        self.filter_collinear |= filter_collinear

        self.__intersection__("_selected_features", list(X_train.columns))
        self.__union__("_filtered_out_features", list(set(self.feat_to_check) - set(X_train.columns)))
        return

    def find_constant_features(self, **kwargs):
        """Esegue solo il filtro per le feature costanti.

        Questo metodo è un wrapper attorno al metodo `run`, configurato per attivare specificamente il filtro delle feature costanti e disabilitare tutti gli altri filtri. Aggiorna lo stato dell'istanza  in base ai risultati di questo singolo filtro.

        Questa funzione ha lo scopo di trovare le colonne che hanno un numero di valori distinti uguale a 1. Se una colonna ha un solo valore distinto, significa che è costante (ad esempio, una colonna dove ogni riga ha il valore `True`), e il nome di questa colonna viene incluso nella lista dei risultati, ovvero tutte le feature da escludere.

        Dopo l'applicazione del filtro vengono modificati gli attributi della classe con la selezione effettuata.

        Args:
            **kwargs: Argomenti keyword aggiuntivi per sovrascrivere i parametri dell'istanza per questa esecuzione (anche se per le feature costanti non ci sono parametri specifici).

        **Dati utilizzati per gli esempi:**

            >>> db_test_filters

            .. raw:: html

                <style>
                   /* Stile base per la tabella con la nostra classe specifica */
                   .jupyter-style-table {
                       border-collapse: collapse; /* Bordi uniti */
                       margin: 1em 0; /* Margine sopra/sotto */
                       font-family: "Helvetica Neue", Helvetica, Arial, sans-serif; /* Font simile a Jupyter */
                       font-size: 0.9em; /* Dimensione font leggermente ridotta */
                       border: 1px solid #d3d3d3; /* Bordo esterno leggero */
                       width: auto; /* Larghezza basata sul contenuto */
                       max-width: 100%; /* Non superare il contenitore */
                       overflow-x: auto; /* Abilita lo scroll orizzontale se necessario (meglio sul wrapper, ma ok qui) */
                       display: block; /* Necessario per far funzionare overflow-x su una tabella */
                   }

                   /* Stile per le celle dell'header (th) */
                   .jupyter-style-table thead th {
                       background-color: #f5f5f5; /* Sfondo grigio chiaro per header */
                       font-weight: bold; /* Grassetto */
                       padding: 8px 10px; /* Padding interno */
                       text-align: right; /* Allineamento testo (spesso a destra per numeri/default) */
                       border-bottom: 1px solid #d3d3d3; /* Linea sotto l'header */
                       vertical-align: bottom; /* Allineamento verticale */
                   }

                   /* Stile per le celle dei dati (td) */
                   .jupyter-style-table tbody td {
                       padding: 6px 10px; /* Padding interno */
                       text-align: right; /* Allineamento testo (aggiusta se hai testo a sinistra) */
                       border-right: 1px solid #d3d3d3; /* Linea verticale tra celle (opzionale) */
                       border-top: 1px solid #d3d3d3; /* Linea orizzontale tra righe */
                       vertical-align: middle; /* Allineamento verticale */
                   }
                   .jupyter-style-table tbody td:last-child {
                       border-right: none; /* Rimuovi bordo destro sull'ultima cella */
                   }

                   /* Stile per l'header dell'indice (se presente) */
                   .jupyter-style-table thead th.blank { /* Header vuoto sopra l'indice */
                       background-color: white;
                       border: none;
                   }
                   .jupyter-style-table tbody th { /* Celle dell'indice nel body */
                       padding: 6px 10px;
                       text-align: right;
                       font-weight: normal;
                       border-right: 1px solid #d3d3d3;
                       border-top: 1px solid #d3d3d3;
                       background-color: #f5f5f5; /* Sfondo leggero per indice */
                   }


                   /* Striping delle righe (alternanza colori) */
                   .jupyter-style-table tbody tr:nth-child(even) {
                       background-color: #f9f9f9; /* Sfondo molto leggero per righe pari */
                   }

                   /* Effetto Hover (cambio colore al passaggio del mouse) */
                   .jupyter-style-table tbody tr:hover {
                       background-color: #f0f0f0; /* Sfondo leggermente più scuro su hover */
                   }
                </style>
                <table border="0" class="jupyter-style-table"><thead><tr style="text-align: right;"><th></th><th>feature_A</th><th>feature_B</th><th>feature_C</th></tr></thead><tbody><tr><th>0</th><td>5</td><td>34.835708</td><td>Z</td></tr><tr><th>1</th><td>5</td><td>3.086785</td><td>X</td></tr><tr><th>2</th><td>5</td><td>42.384427</td><td>Y</td></tr><tr><th>3</th><td>5</td><td>86.151493</td><td>X</td></tr><tr><th>4</th><td>5</td><td>-1.707669</td><td>V</td></tr><tr><th>5</th><td>5</td><td>-1.706848</td><td>V</td></tr><tr><th>6</th><td>5</td><td>88.960641</td><td>X</td></tr><tr><th>7</th><td>5</td><td>48.371736</td><td>V</td></tr><tr><th>8</th><td>5</td><td>-13.473719</td><td>Z</td></tr><tr><th>9</th><td>5</td><td>37.128002</td><td>Y</td></tr><tr><th>10</th><td>5</td><td>-13.170885</td><td>X</td></tr><tr><th>11</th><td>5</td><td>-13.286488</td><td>Z</td></tr><tr><th>12</th><td>5</td><td>22.098114</td><td>W</td></tr><tr><th>13</th><td>5</td><td>-85.664012</td><td>W</td></tr><tr><th>14</th><td>5</td><td>-76.245892</td><td>X</td></tr><tr><th>15</th><td>5</td><td>-18.114376</td><td>X</td></tr><tr><th>16</th><td>5</td><td>-40.641556</td><td>Z</td></tr><tr><th>17</th><td>5</td><td>25.712367</td><td>Y</td></tr><tr><th>18</th><td>5</td><td>-35.401204</td><td>Y</td></tr><tr><th>19</th><td>5</td><td>-60.615185</td><td>Y</td></tr></tbody></table>

        **Esempio:**

        >>> from cefeste.selection import FeatureSelection
        >>> fs = FeatureSelection(
        ...    db=df_test_filters,
        ...    verbose=True # Utile per vedere cosa succede
        ... )
        >>> fs.find_constant_features()
        >>> fs.make_report()

        .. raw:: html

            <table border="0" class="jupyter-style-table">  <thead>    <tr style="text-align: right;">      <th></th>      <th>feat_name</th>      <th>result</th>      <th>drop_reason</th>    </tr>  </thead>  <tbody>    <tr>      <th>0</th>      <td>feature_A</td>      <td>drop</td>      <td>constant</td>    </tr>    <tr>      <th>1</th>      <td>feature_B</td>      <td>keep</td>      <td>NaN</td>    </tr>    <tr>      <th>2</th>      <td>feature_C</td>      <td>keep</td>      <td>NaN</td>    </tr>  </tbody></table>
        """
        self.run(
            filter_constant=True,
            filter_missing=False,
            filter_highly_concentrated=False,
            filter_low_values=False,
            filter_unstable=False,
            filter_unexplanatory=False,
            filter_correlated=False,
            filter_collinear=False,
            **kwargs,
        )
        return

    def find_missing_features(self, **kwargs):
        """Esegue solo il filtro per le feature con troppi valori mancanti.

        Questo metodo è un wrapper attorno al metodo `run`, configurato per attivare specificamente il filtro delle feature con valori mancanti e disabilitare tutti gli altri filtri. Aggiorna lo stato dell'istanza in base ai risultati di questo singolo filtro.

        Questa funzione individua le colonne che hanno una percentuale di valori mancanti (o "missing", come NaN o None) superiore a una soglia definita (`max_pct_missing`, default 0,9). Se, ad esempio, più del 90% dei valori in una colonna sono mancanti e la soglia è 0.9 (cioè 90%), il nome di quella colonna verrà rimosso.

        Dopo l'applicazione del filtro vengono modificati gli attributi della classe con la selezione effettuata.

        Args:
            **kwargs: Argomenti keyword aggiuntivi per sovrascrivere i parametri dell'istanza per questa esecuzione.

        **Dati utilizzati per gli esempi:**

            >>> db_test_filters

            .. raw:: html

                <style>
                   /* Stile base per la tabella con la nostra classe specifica */
                   .jupyter-style-table {
                       border-collapse: collapse; /* Bordi uniti */
                       margin: 1em 0; /* Margine sopra/sotto */
                       font-family: "Helvetica Neue", Helvetica, Arial, sans-serif; /* Font simile a Jupyter */
                       font-size: 0.9em; /* Dimensione font leggermente ridotta */
                       border: 1px solid #d3d3d3; /* Bordo esterno leggero */
                       width: auto; /* Larghezza basata sul contenuto */
                       max-width: 100%; /* Non superare il contenitore */
                       overflow-x: auto; /* Abilita lo scroll orizzontale se necessario (meglio sul wrapper, ma ok qui) */
                       display: block; /* Necessario per far funzionare overflow-x su una tabella */
                   }

                   /* Stile per le celle dell'header (th) */
                   .jupyter-style-table thead th {
                       background-color: #f5f5f5; /* Sfondo grigio chiaro per header */
                       font-weight: bold; /* Grassetto */
                       padding: 8px 10px; /* Padding interno */
                       text-align: right; /* Allineamento testo (spesso a destra per numeri/default) */
                       border-bottom: 1px solid #d3d3d3; /* Linea sotto l'header */
                       vertical-align: bottom; /* Allineamento verticale */
                   }

                   /* Stile per le celle dei dati (td) */
                   .jupyter-style-table tbody td {
                       padding: 6px 10px; /* Padding interno */
                       text-align: right; /* Allineamento testo (aggiusta se hai testo a sinistra) */
                       border-right: 1px solid #d3d3d3; /* Linea verticale tra celle (opzionale) */
                       border-top: 1px solid #d3d3d3; /* Linea orizzontale tra righe */
                       vertical-align: middle; /* Allineamento verticale */
                   }
                   .jupyter-style-table tbody td:last-child {
                       border-right: none; /* Rimuovi bordo destro sull'ultima cella */
                   }

                   /* Stile per l'header dell'indice (se presente) */
                   .jupyter-style-table thead th.blank { /* Header vuoto sopra l'indice */
                       background-color: white;
                       border: none;
                   }
                   .jupyter-style-table tbody th { /* Celle dell'indice nel body */
                       padding: 6px 10px;
                       text-align: right;
                       font-weight: normal;
                       border-right: 1px solid #d3d3d3;
                       border-top: 1px solid #d3d3d3;
                       background-color: #f5f5f5; /* Sfondo leggero per indice */
                   }


                   /* Striping delle righe (alternanza colori) */
                   .jupyter-style-table tbody tr:nth-child(even) {
                       background-color: #f9f9f9; /* Sfondo molto leggero per righe pari */
                   }

                   /* Effetto Hover (cambio colore al passaggio del mouse) */
                   .jupyter-style-table tbody tr:hover {
                       background-color: #f0f0f0; /* Sfondo leggermente più scuro su hover */
                   }
                </style>
                <table border="0" class="jupyter-style-table"><thead><tr style="text-align: right;"><th></th><th>feature_A</th><th>feature_B</th><th>feature_C</th></tr></thead><tbody><tr><th>0</th><td>NaN</td><td>25.131773</td><td>X</td></tr><tr><th>1</th><td>NaN</td><td>-27.713793</td><td>X</td></tr><tr><th>2</th><td>NaN</td><td>6.793083</td><td>Z</td></tr><tr><th>3</th><td>NaN</td><td>26.438121</td><td>Y</td></tr><tr><th>4</th><td>NaN</td><td>26.067861</td><td>X</td></tr><tr><th>5</th><td>NaN</td><td>31.096038</td><td>Z</td></tr><tr><th>6</th><td>NaN</td><td>90.685563</td><td>X</td></tr><tr><th>7</th><td>NaN</td><td>32.676715</td><td>W</td></tr><tr><th>8</th><td>NaN</td><td>-2.207832</td><td>Y</td></tr><tr><th>9</th><td>NaN</td><td>58.204358</td><td>X</td></tr><tr><th>10</th><td>NaN</td><td>69.473524</td><td>Z</td></tr><tr><th>11</th><td>NaN</td><td>-51.380391</td><td>Y</td></tr><tr><th>12</th><td>NaN</td><td>39.870003</td><td>V</td></tr><tr><th>13</th><td>NaN</td><td>45.058637</td><td>Z</td></tr><tr><th>14</th><td>NaN</td><td>-4.878175</td><td>Y</td></tr><tr><th>15</th><td>9.0</td><td>78.785341</td><td>W</td></tr><tr><th>16</th><td>NaN</td><td>2.497221</td><td>Y</td></tr><tr><th>17</th><td>NaN</td><td>16.278823</td><td>V</td></tr><tr><th>18</th><td>NaN</td><td>1.346409</td><td>Y</td></tr><tr><th>19</th><td>NaN</td><td>10.778952</td><td>Z</td></tr></tbody></table>

        **Esempio:**

        >>> from cefeste.selection import FeatureSelection
        >>> fs = FeatureSelection(
        ...    db=df_test_filters,
        ...    verbose=True # Utile per vedere cosa succede
        ... )
        >>> fs.find_missing_features()
        >>> fs.make_report()

        .. raw:: html

            <table border="0" class="jupyter-style-table">  <thead>    <tr style="text-align: right;">      <th></th>      <th>feat_name</th>      <th>result</th>      <th>drop_reason</th>    </tr>  </thead>  <tbody>    <tr>      <th>0</th>      <td>feature_A</td>      <td>drop</td>      <td>missing</td>    </tr>    <tr>      <th>1</th>      <td>feature_B</td>      <td>keep</td>      <td>NaN</td>    </tr>    <tr>      <th>2</th>      <td>feature_C</td>      <td>keep</td>      <td>NaN</td>    </tr>  </tbody></table>
        """
        self.run(
            filter_constant=False,
            filter_missing=True,
            filter_highly_concentrated=False,
            filter_low_values=False,
            filter_unstable=False,
            filter_unexplanatory=False,
            filter_correlated=False,
            filter_collinear=False,
            **kwargs,
        )
        return

    def find_high_topcat_features(self, **kwargs):
        """Esegue solo il filtro per le feature  altamente concentrate.

        Questo metodo è un wrapper attorno al metodo `run`, configurato per attivare specificamente il filtro delle feature altamente concentrate e disabilitare tutti gli altri filtri. Aggiorna lo stato dell'istanza in base ai risultati di questo singolo filtro.

        Questa funzione identifica le colonne dove un singolo valore (il valore più frequente) appare in una percentuale eccessivamente alta di osservazioni. Per ogni colonna, calcola la frequenza di ogni suo valore. Se questa frequenza supera la soglia specificata (`max_pct_mfv`, default 0,95), il nome della colonna viene aggiunto alla lista dei risultati.

        Dopo l'applicazione del filtro vengono modificati gli attributi della classe con la selezione effettuata.

        Args:
            **kwargs: Argomenti keyword aggiuntivi per sovrascrivere i parametri dell'istanza per questa esecuzione.

        **Dati utilizzati per gli esempi:**

            >>> db_test_filters

            .. raw:: html

                <style>
                   /* Stile base per la tabella con la nostra classe specifica */
                   .jupyter-style-table {
                       border-collapse: collapse; /* Bordi uniti */
                       margin: 1em 0; /* Margine sopra/sotto */
                       font-family: "Helvetica Neue", Helvetica, Arial, sans-serif; /* Font simile a Jupyter */
                       font-size: 0.9em; /* Dimensione font leggermente ridotta */
                       border: 1px solid #d3d3d3; /* Bordo esterno leggero */
                       width: auto; /* Larghezza basata sul contenuto */
                       max-width: 100%; /* Non superare il contenitore */
                       overflow-x: auto; /* Abilita lo scroll orizzontale se necessario (meglio sul wrapper, ma ok qui) */
                       display: block; /* Necessario per far funzionare overflow-x su una tabella */
                   }

                   /* Stile per le celle dell'header (th) */
                   .jupyter-style-table thead th {
                       background-color: #f5f5f5; /* Sfondo grigio chiaro per header */
                       font-weight: bold; /* Grassetto */
                       padding: 8px 10px; /* Padding interno */
                       text-align: right; /* Allineamento testo (spesso a destra per numeri/default) */
                       border-bottom: 1px solid #d3d3d3; /* Linea sotto l'header */
                       vertical-align: bottom; /* Allineamento verticale */
                   }

                   /* Stile per le celle dei dati (td) */
                   .jupyter-style-table tbody td {
                       padding: 6px 10px; /* Padding interno */
                       text-align: right; /* Allineamento testo (aggiusta se hai testo a sinistra) */
                       border-right: 1px solid #d3d3d3; /* Linea verticale tra celle (opzionale) */
                       border-top: 1px solid #d3d3d3; /* Linea orizzontale tra righe */
                       vertical-align: middle; /* Allineamento verticale */
                   }
                   .jupyter-style-table tbody td:last-child {
                       border-right: none; /* Rimuovi bordo destro sull'ultima cella */
                   }

                   /* Stile per l'header dell'indice (se presente) */
                   .jupyter-style-table thead th.blank { /* Header vuoto sopra l'indice */
                       background-color: white;
                       border: none;
                   }
                   .jupyter-style-table tbody th { /* Celle dell'indice nel body */
                       padding: 6px 10px;
                       text-align: right;
                       font-weight: normal;
                       border-right: 1px solid #d3d3d3;
                       border-top: 1px solid #d3d3d3;
                       background-color: #f5f5f5; /* Sfondo leggero per indice */
                   }


                   /* Striping delle righe (alternanza colori) */
                   .jupyter-style-table tbody tr:nth-child(even) {
                       background-color: #f9f9f9; /* Sfondo molto leggero per righe pari */
                   }

                   /* Effetto Hover (cambio colore al passaggio del mouse) */
                   .jupyter-style-table tbody tr:hover {
                       background-color: #f0f0f0; /* Sfondo leggermente più scuro su hover */
                   }
                </style>
                <table border="0" class="jupyter-style-table"><thead><tr style="text-align: right;"><th></th><th>feature_A</th><th>feature_B</th><th>feature_C</th></tr></thead><tbody><tr><th>0</th><td>A</td><td>-54.734074</td><td>Z</td></tr><tr><th>1</th><td>A</td><td>68.041339</td><td>W</td></tr><tr><th>2</th><td>A</td><td>-13.385060</td><td>V</td></tr><tr><th>3</th><td>A</td><td>27.325194</td><td>Y</td></tr><tr><th>4</th><td>A</td><td>7.653971</td><td>V</td></tr><tr><th>5</th><td>A</td><td>33.852041</td><td>V</td></tr><tr><th>6</th><td>A</td><td>13.841095</td><td>V</td></tr><tr><th>7</th><td>B</td><td>-54.149611</td><td>W</td></tr><tr><th>8</th><td>C</td><td>59.813341</td><td>W</td></tr><tr><th>9</th><td>D</td><td>-14.687829</td><td>Z</td></tr><tr><th>10</th><td>A</td><td>-67.829095</td><td>W</td></tr><tr><th>11</th><td>A</td><td>-11.405758</td><td>Z</td></tr><tr><th>12</th><td>A</td><td>85.037990</td><td>W</td></tr><tr><th>13</th><td>A</td><td>52.511087</td><td>Z</td></tr><tr><th>14</th><td>A</td><td>-7.432607</td><td>W</td></tr><tr><th>15</th><td>A</td><td>-7.462885</td><td>V</td></tr><tr><th>16</th><td>A</td><td>-6.081753</td><td>X</td></tr><tr><th>17</th><td>A</td><td>113.837399</td><td>V</td></tr><tr><th>18</th><td>A</td><td>29.096773</td><td>Z</td></tr><tr><th>19</th><td>A</td><td>31.502082</td><td>V</td></tr></tbody></table>

        **Esempio:**

        >>> from cefeste.selection import FeatureSelection
        >>> fs = FeatureSelection(
        ...    db=df_test_filters,
        ...    verbose=True # Utile per vedere cosa succede
        ... )
        >>> fs.find_high_topcat_features(max_pct_mfv=0.75)
        >>> fs.make_report()

        .. raw:: html

            <table border="0" class="jupyter-style-table">  <thead>    <tr style="text-align: right;">      <th></th>      <th>feat_name</th>      <th>result</th>      <th>drop_reason</th>    </tr>  </thead>  <tbody>    <tr>      <th>0</th>      <td>feature_A</td>      <td>drop</td>      <td>highly_concentrated</td>    </tr>    <tr>      <th>1</th>      <td>feature_B</td>      <td>keep</td>      <td>NaN</td>    </tr>    <tr>      <th>2</th>      <td>feature_C</td>      <td>keep</td>      <td>NaN</td>    </tr>  </tbody></table>
        """
        self.run(
            filter_constant=False,
            filter_missing=False,
            filter_highly_concentrated=True,
            filter_low_values=False,
            filter_unstable=False,
            filter_unexplanatory=False,
            filter_correlated=False,
            filter_collinear=False,
            **kwargs,
        )
        return

    def find_low_nvalues_features(self, **kwargs):
        """Esegue solo il filtro per le feature con un basso numero di valori unici.

        Questo metodo è un wrapper attorno al metodo `run`, configurato per attivare specificamente il filtro delle feature con un basso numero di valori unici e disabilitare tutti gli altri filtri. Aggiorna lo stato dell'istanza in base ai risultati di questo singolo filtro.

        Questa funzione trova le colonne che hanno un numero di valori distinti inferiore a una soglia specificata (`min_unique_val`, default 3). Ad esempio, se si imposta `min_unique_val` a 3, la funzione identificherà tutte le colonne che presentano solo 1 o 2 valori unici. Se la soglia è 2, il risultato è identico a quello del metodo `find_constant_features`. I nomi di queste colonne con pochi valori distinti vengono rimossi.

        Dopo l'applicazione del filtro vengono modificati gli attributi della classe con la selezione effettuata.

        Args:
            **kwargs: Argomenti keyword aggiuntivi per sovrascrivere i parametri dell'istanza per questa esecuzione.

        **Dati utilizzati per gli esempi:**

            >>> db_test_filters

            .. raw:: html

                <style>
                   /* Stile base per la tabella con la nostra classe specifica */
                   .jupyter-style-table {
                       border-collapse: collapse; /* Bordi uniti */
                       margin: 1em 0; /* Margine sopra/sotto */
                       font-family: "Helvetica Neue", Helvetica, Arial, sans-serif; /* Font simile a Jupyter */
                       font-size: 0.9em; /* Dimensione font leggermente ridotta */
                       border: 1px solid #d3d3d3; /* Bordo esterno leggero */
                       width: auto; /* Larghezza basata sul contenuto */
                       max-width: 100%; /* Non superare il contenitore */
                       overflow-x: auto; /* Abilita lo scroll orizzontale se necessario (meglio sul wrapper, ma ok qui) */
                       display: block; /* Necessario per far funzionare overflow-x su una tabella */
                   }

                   /* Stile per le celle dell'header (th) */
                   .jupyter-style-table thead th {
                       background-color: #f5f5f5; /* Sfondo grigio chiaro per header */
                       font-weight: bold; /* Grassetto */
                       padding: 8px 10px; /* Padding interno */
                       text-align: right; /* Allineamento testo (spesso a destra per numeri/default) */
                       border-bottom: 1px solid #d3d3d3; /* Linea sotto l'header */
                       vertical-align: bottom; /* Allineamento verticale */
                   }

                   /* Stile per le celle dei dati (td) */
                   .jupyter-style-table tbody td {
                       padding: 6px 10px; /* Padding interno */
                       text-align: right; /* Allineamento testo (aggiusta se hai testo a sinistra) */
                       border-right: 1px solid #d3d3d3; /* Linea verticale tra celle (opzionale) */
                       border-top: 1px solid #d3d3d3; /* Linea orizzontale tra righe */
                       vertical-align: middle; /* Allineamento verticale */
                   }
                   .jupyter-style-table tbody td:last-child {
                       border-right: none; /* Rimuovi bordo destro sull'ultima cella */
                   }

                   /* Stile per l'header dell'indice (se presente) */
                   .jupyter-style-table thead th.blank { /* Header vuoto sopra l'indice */
                       background-color: white;
                       border: none;
                   }
                   .jupyter-style-table tbody th { /* Celle dell'indice nel body */
                       padding: 6px 10px;
                       text-align: right;
                       font-weight: normal;
                       border-right: 1px solid #d3d3d3;
                       border-top: 1px solid #d3d3d3;
                       background-color: #f5f5f5; /* Sfondo leggero per indice */
                   }


                   /* Striping delle righe (alternanza colori) */
                   .jupyter-style-table tbody tr:nth-child(even) {
                       background-color: #f9f9f9; /* Sfondo molto leggero per righe pari */
                   }

                   /* Effetto Hover (cambio colore al passaggio del mouse) */
                   .jupyter-style-table tbody tr:hover {
                       background-color: #f0f0f0; /* Sfondo leggermente più scuro su hover */
                   }
                </style>
                <table border="0" class="jupyter-style-table"><thead><tr style="text-align: right;"><th></th><th>feature_A</th><th>feature_B</th><th>feature_C</th></tr></thead><tbody><tr><th>0</th><td>A</td><td>34.835708</td><td>Z</td></tr><tr><th>1</th><td>B</td><td>3.086785</td><td>X</td></tr><tr><th>2</th><td>A</td><td>42.384427</td><td>Y</td></tr><tr><th>3</th><td>B</td><td>86.151493</td><td>X</td></tr><tr><th>4</th><td>A</td><td>-1.707669</td><td>V</td></tr><tr><th>5</th><td>B</td><td>-1.706848</td><td>V</td></tr><tr><th>6</th><td>A</td><td>88.960641</td><td>X</td></tr><tr><th>7</th><td>B</td><td>48.371736</td><td>V</td></tr><tr><th>8</th><td>A</td><td>-13.473719</td><td>Z</td></tr><tr><th>9</th><td>B</td><td>37.128002</td><td>Y</td></tr><tr><th>10</th><td>A</td><td>-13.170885</td><td>X</td></tr><tr><th>11</th><td>B</td><td>-13.286488</td><td>Z</td></tr><tr><th>12</th><td>A</td><td>22.098114</td><td>W</td></tr><tr><th>13</th><td>B</td><td>-85.664012</td><td>W</td></tr><tr><th>14</th><td>A</td><td>-76.245892</td><td>X</td></tr><tr><th>15</th><td>B</td><td>-18.114376</td><td>X</td></tr><tr><th>16</th><td>A</td><td>-40.641556</td><td>Z</td></tr><tr><th>17</th><td>B</td><td>25.712367</td><td>Y</td></tr><tr><th>18</th><td>A</td><td>-35.401204</td><td>Y</td></tr><tr><th>19</th><td>B</td><td>-60.615185</td><td>Y</td></tr></tbody></table>

        **Esempio:**

        >>> from cefeste.selection import FeatureSelection
        >>> fs = FeatureSelection(
        ...    db=df_test_filters,
        ...    verbose=True # Utile per vedere cosa succede
        ... )
        >>> fs.find_low_nvalues_features()
        >>> fs.make_report()

        .. raw:: html

            <table border="0" class="jupyter-style-table">  <thead>    <tr style="text-align: right;">      <th></th>      <th>feat_name</th>      <th>result</th>      <th>drop_reason</th>    </tr>  </thead>  <tbody>    <tr>      <th>0</th>      <td>feature_A</td>      <td>drop</td>      <td>low_values</td>    </tr>    <tr>      <th>1</th>      <td>feature_B</td>      <td>keep</td>      <td>NaN</td>    </tr>    <tr>      <th>2</th>      <td>feature_C</td>      <td>keep</td>      <td>NaN</td>    </tr>  </tbody></table>
        """
        self.run(
            filter_constant=False,
            filter_missing=False,
            filter_highly_concentrated=False,
            filter_low_values=True,
            filter_unstable=False,
            filter_unexplanatory=False,
            filter_correlated=False,
            filter_collinear=False,
        )
        return

    def find_unstable_psi_features(self, **kwargs):
        """Esegue solo il filtro per le feature instabili (basato su PSI).

        Questo metodo è un wrapper attorno al metodo `run`, configurato per attivare specificamente il filtro delle feature instabili tra campioni (misurate tramite Population Stability Index) e disabilitare tutti gli altri filtri. Aggiorna lo stato dell'istanza in base ai risultati di questo singolo filtro.

        Questa funzione confronta la distribuzione dei valori di ciascuna colonna tra le due sezioni del `DataFrame` (una relativa al train e una al test). Lo scopo è identificare le colonne la cui distribuzione dei dati è cambiata in modo significativo tra i due set. Se il cambiamento (misurato internamente con un indice chiamato PSI - Population Stability Index) supera una certa soglia (`max_psi`, default 0.2), la colonna è considerata "instabile" e il suo nome viene restituito. Oltre alla soglia possono essere impostati parametri aggiuntivi come la percentuale minima di valori all'interno di un bin (`psi_bin_min_pct`, default 0.2) e il numero massimo di bin da utilizzare per il calcolo (`psi_nbins`, default 20).

        Dopo l'applicazione del filtro vengono modificati gli attributi della classe con la selezione effettuata.

        Args:
            **kwargs: Argomenti keyword aggiuntivi per sovrascrivere i parametri dell'istanza per questa esecuzione.

        **Dati utilizzati per gli esempi:**

            >>> db_test_filters

            .. raw:: html

                <style>
                   /* Stile base per la tabella con la nostra classe specifica */
                   .jupyter-style-table {
                       border-collapse: collapse; /* Bordi uniti */
                       margin: 1em 0; /* Margine sopra/sotto */
                       font-family: "Helvetica Neue", Helvetica, Arial, sans-serif; /* Font simile a Jupyter */
                       font-size: 0.9em; /* Dimensione font leggermente ridotta */
                       border: 1px solid #d3d3d3; /* Bordo esterno leggero */
                       width: auto; /* Larghezza basata sul contenuto */
                       max-width: 100%; /* Non superare il contenitore */
                       overflow-x: auto; /* Abilita lo scroll orizzontale se necessario (meglio sul wrapper, ma ok qui) */
                       display: block; /* Necessario per far funzionare overflow-x su una tabella */
                   }

                   /* Stile per le celle dell'header (th) */
                   .jupyter-style-table thead th {
                       background-color: #f5f5f5; /* Sfondo grigio chiaro per header */
                       font-weight: bold; /* Grassetto */
                       padding: 8px 10px; /* Padding interno */
                       text-align: right; /* Allineamento testo (spesso a destra per numeri/default) */
                       border-bottom: 1px solid #d3d3d3; /* Linea sotto l'header */
                       vertical-align: bottom; /* Allineamento verticale */
                   }

                   /* Stile per le celle dei dati (td) */
                   .jupyter-style-table tbody td {
                       padding: 6px 10px; /* Padding interno */
                       text-align: right; /* Allineamento testo (aggiusta se hai testo a sinistra) */
                       border-right: 1px solid #d3d3d3; /* Linea verticale tra celle (opzionale) */
                       border-top: 1px solid #d3d3d3; /* Linea orizzontale tra righe */
                       vertical-align: middle; /* Allineamento verticale */
                   }
                   .jupyter-style-table tbody td:last-child {
                       border-right: none; /* Rimuovi bordo destro sull'ultima cella */
                   }

                   /* Stile per l'header dell'indice (se presente) */
                   .jupyter-style-table thead th.blank { /* Header vuoto sopra l'indice */
                       background-color: white;
                       border: none;
                   }
                   .jupyter-style-table tbody th { /* Celle dell'indice nel body */
                       padding: 6px 10px;
                       text-align: right;
                       font-weight: normal;
                       border-right: 1px solid #d3d3d3;
                       border-top: 1px solid #d3d3d3;
                       background-color: #f5f5f5; /* Sfondo leggero per indice */
                   }


                   /* Striping delle righe (alternanza colori) */
                   .jupyter-style-table tbody tr:nth-child(even) {
                       background-color: #f9f9f9; /* Sfondo molto leggero per righe pari */
                   }

                   /* Effetto Hover (cambio colore al passaggio del mouse) */
                   .jupyter-style-table tbody tr:hover {
                       background-color: #f0f0f0; /* Sfondo leggermente più scuro su hover */
                   }
                </style>
                <table border="0" class="jupyter-style-table"><thead><tr style="text-align: right;"><th></th><th>feature_B</th><th>feature_C</th><th>sample_col</th><th>feature_A</th></tr></thead><tbody><tr><th>0</th><td>34.835708</td><td>Z</td><td>test</td><td>0.123</td></tr><tr><th>1</th><td>3.086785</td><td>X</td><td>test</td><td>0.456</td></tr><tr><th>2</th><td>42.384427</td><td>Y</td><td>test</td><td>0.789</td></tr><tr><th>3</th><td>86.151493</td><td>X</td><td>test</td><td>0.987</td></tr><tr><th>4</th><td>-1.707669</td><td>V</td><td>test</td><td>0.654</td></tr><tr><th>5</th><td>-1.706848</td><td>V</td><td>test</td><td>0.321</td></tr><tr><th>6</th><td>88.960641</td><td>X</td><td>test</td><td>0.234</td></tr><tr><th>7</th><td>48.371736</td><td>V</td><td>test</td><td>0.567</td></tr><tr><th>8</th><td>-13.473719</td><td>Z</td><td>test</td><td>0.890</td></tr><tr><th>9</th><td>37.128002</td><td>Y</td><td>test</td><td>0.012</td></tr><tr><th>10</th><td>-13.170885</td><td>X</td><td>train</td><td>55.0</td></tr><tr><th>11</th><td>-13.286488</td><td>Z</td><td>train</td><td>56.0</td></tr><tr><th>12</th><td>22.098114</td><td>W</td><td>train</td><td>50.0</td></tr><tr><th>13</th><td>-85.664012</td><td>W</td><td>train</td><td>55.0</td></tr><tr><th>14</th><td>-76.245892</td><td>X</td><td>train</td><td>57.0</td></tr><tr><th>15</th><td>-18.114376</td><td>X</td><td>train</td><td>54.0</td></tr><tr><th>16</th><td>-40.641556</td><td>Z</td><td>train</td><td>56.0</td></tr><tr><th>17</th><td>25.712367</td><td>Y</td><td>train</td><td>59.0</td></tr><tr><th>18</th><td>-35.401204</td><td>Y</td><td>train</td><td>55.0</td></tr><tr><th>19</th><td>-60.615185</td><td>Y</td><td>train</td><td>53.0</td></tr></tbody></table>

        **Esempio:**

        >>> from cefeste.selection import FeatureSelection
        >>> fs = FeatureSelection(
        ...    db=df_test_filters,
        ...    sample_col='sample_col',
        ...    sample_train_value='train',
        ...    verbose=True # Utile per vedere cosa succede
        ... )
        >>> fs.find_unstable_psi_features()
        >>> fs.make_report()

        .. raw:: html

            <table border="0" class="jupyter-style-table">  <thead>    <tr style="text-align: right;">      <th></th>      <th>feat_name</th>      <th>result</th>      <th>drop_reason</th>    </tr>  </thead>  <tbody>    <tr>      <th>0</th>      <td>feature_A</td>      <td>drop</td>      <td>unstable</td>    </tr>    <tr>      <th>1</th>      <td>feature_B</td>      <td>keep</td>      <td>NaN</td>    </tr>    <tr>      <th>2</th>      <td>feature_C</td>      <td>keep</td>      <td>NaN</td>    </tr>  </tbody></table>
        """
        self.run(
            filter_constant=False,
            filter_missing=False,
            filter_highly_concentrated=False,
            filter_low_values=False,
            filter_unstable=True,
            filter_unexplanatory=False,
            filter_correlated=False,
            filter_collinear=False,
            **kwargs,
        )
        return

    def find_not_explanatory(self, **kwargs):
        """Esegue solo il filtro per le feature non esplicative rispetto al target.

        Questo metodo è un wrapper attorno al metodo `run`, configurato per attivare specificamente il filtro delle feature con basso potere esplicativo e disabilitare tutti gli altri filtri. Aggiorna lo stato dell'istanza in base ai risultati di questo singolo filtro.

        Questa funzione ha l'obiettivo di identificare le feature che, prese singolarmente, non dimostrano una capacità sufficiente di spiegare o predire la variabile target. In pratica, cerca le feature "poco utili" al problema di machine learning. Il modo in cui valuta l'utilità di una feature dipende dal tipo di problema che si sta affrontando, specificato dal parametro `algo_type` (default "classification").

        Indipendentemente dal tipo di problema, la funzione opera esaminando ogni feature una alla volta:

        * Se il tipo di problema è **classification (classificazione binaria)**: Per ogni singola feature nel dataset (eventualmente solo di training), la funzione esegue i seguenti passaggi: prima di tutto, la feature viene preparata. Se è una feature categorica, viene trasformata in un formato numerico (usando One-Hot Encoding, o una sua versione semplificata se la feature ha troppe categorie distinte, specificando il numero di feature desiderate tramite il parametro `dim_cat_threshold`, default 10). Se è una feature numerica, eventuali valori mancanti vengono riempiti (ad esempio, con la mediana). Successivamente, viene addestrato un modello predittivo semplice (un Albero Decisionale) utilizzando esclusivamente quella singola feature preparata per cercare di predire la variabile target (eventualmente solo di training). La capacità predittiva di questo modello basato sulla singola feature viene poi misurata calcolando l'AUC (Area Under the ROC Curve) sia sui dati di training che, se forniti, sui dati di test. Se il valore di AUC ottenuto (o il valore minimo tra training e test, se entrambi disponibili) è inferiore a una certa soglia minima di performance (derivata dal parametro `threshold` sommandogli 1 e dividendo per 2, valore default di `threshold` 0.05), allora quella feature viene considerata "non esplicativa" e il suo nome viene aggiunto a una lista di feature da scartare.

        * Se il tipo di problema è **regression (regressione)**: Anche in questo caso, ogni feature viene analizzata individualmente. Se la feature è categorica, si calcola una misura di associazione (simile alla correlazione tra feature miste, per dettagli vedere :meth:`~cefeste.selection.FeatureSelection.find_correlated_features`) tra quella feature (dopo aver gestito i valori mancanti) e la variabile target numerica (eventualmente anche di test). Se la feature è numerica, si calcola la correlazione di Pearson (in valore assoluto) tra la feature (dopo aver gestito i valori mancanti) e la variabile target. Se questa misura di correlazione/associazione (o il valore minimo tra training e test, se entrambi disponibili) risulta inferiore a una certa soglia (`threshold`, default 0,05), la feature viene etichettata come "non esplicativa".

        * Se il tipo di problema è **multiclass (classificazione multiclasse)**: Il processo è molto simile a quello della classificazione binaria. Per ogni singola feature, dopo la preparazione (gestione delle categoriche con One-Hot Encoding/semplificato e riempimento dei mancanti per le numeriche), si addestra un Albero Decisionale usando solo quella feature per predire la variabile target multiclasse. La performance viene misurata tramite l'AUC, adattato per problemi multiclasse (ad esempio, calcolando l'AUC in modalità "one-vs-rest"). Questo viene fatto per i dati di training e, se presenti, per quelli di test. Se l'AUC (o il minimo tra training e test) non raggiunge la soglia minima richiesta (derivata dal parametro `threshold` sommandogli 1 e dividendo per 2, valore default di `threshold` 0.05), la feature è considerata "non esplicativa".

        Dopo l'applicazione del filtro vengono modificati gli attributi della classe con la selezione effettuata.

        Args:
            **kwargs: Argomenti keyword aggiuntivi per sovrascrivere i parametri dell'istanza per questa esecuzione.

        **Dati utilizzati per gli esempi:**

            >>> db_test_filters

            .. raw:: html

                <style>
                   /* Stile base per la tabella con la nostra classe specifica */
                   .jupyter-style-table {
                       border-collapse: collapse; /* Bordi uniti */
                       margin: 1em 0; /* Margine sopra/sotto */
                       font-family: "Helvetica Neue", Helvetica, Arial, sans-serif; /* Font simile a Jupyter */
                       font-size: 0.9em; /* Dimensione font leggermente ridotta */
                       border: 1px solid #d3d3d3; /* Bordo esterno leggero */
                       width: auto; /* Larghezza basata sul contenuto */
                       max-width: 100%; /* Non superare il contenitore */
                       overflow-x: auto; /* Abilita lo scroll orizzontale se necessario (meglio sul wrapper, ma ok qui) */
                       display: block; /* Necessario per far funzionare overflow-x su una tabella */
                   }

                   /* Stile per le celle dell'header (th) */
                   .jupyter-style-table thead th {
                       background-color: #f5f5f5; /* Sfondo grigio chiaro per header */
                       font-weight: bold; /* Grassetto */
                       padding: 8px 10px; /* Padding interno */
                       text-align: right; /* Allineamento testo (spesso a destra per numeri/default) */
                       border-bottom: 1px solid #d3d3d3; /* Linea sotto l'header */
                       vertical-align: bottom; /* Allineamento verticale */
                   }

                   /* Stile per le celle dei dati (td) */
                   .jupyter-style-table tbody td {
                       padding: 6px 10px; /* Padding interno */
                       text-align: right; /* Allineamento testo (aggiusta se hai testo a sinistra) */
                       border-right: 1px solid #d3d3d3; /* Linea verticale tra celle (opzionale) */
                       border-top: 1px solid #d3d3d3; /* Linea orizzontale tra righe */
                       vertical-align: middle; /* Allineamento verticale */
                   }
                   .jupyter-style-table tbody td:last-child {
                       border-right: none; /* Rimuovi bordo destro sull'ultima cella */
                   }

                   /* Stile per l'header dell'indice (se presente) */
                   .jupyter-style-table thead th.blank { /* Header vuoto sopra l'indice */
                       background-color: white;
                       border: none;
                   }
                   .jupyter-style-table tbody th { /* Celle dell'indice nel body */
                       padding: 6px 10px;
                       text-align: right;
                       font-weight: normal;
                       border-right: 1px solid #d3d3d3;
                       border-top: 1px solid #d3d3d3;
                       background-color: #f5f5f5; /* Sfondo leggero per indice */
                   }


                   /* Striping delle righe (alternanza colori) */
                   .jupyter-style-table tbody tr:nth-child(even) {
                       background-color: #f9f9f9; /* Sfondo molto leggero per righe pari */
                   }

                   /* Effetto Hover (cambio colore al passaggio del mouse) */
                   .jupyter-style-table tbody tr:hover {
                       background-color: #f0f0f0; /* Sfondo leggermente più scuro su hover */
                   }
                </style>
                <table border="0" class="jupyter-style-table"><thead><tr style="text-align: right;"><th></th><th>feature_A</th><th>feature_B</th><th>feature_C</th><th>target</th></tr></thead><tbody><tr><th>0</th><td>A</td><td>34.835708</td><td>Z</td><td>75.013312</td></tr><tr><th>1</th><td>B</td><td>3.086785</td><td>X</td><td>109.194174</td></tr><tr><th>2</th><td>C</td><td>42.384427</td><td>Y</td><td>96.287048</td></tr><tr><th>3</th><td>D</td><td>86.151493</td><td>X</td><td>264.905765</td></tr><tr><th>4</th><td>E</td><td>-1.707669</td><td>V</td><td>2.880829</td></tr><tr><th>5</th><td>A</td><td>-1.706848</td><td>V</td><td>2.318509</td></tr><tr><th>6</th><td>B</td><td>88.960641</td><td>X</td><td>273.054387</td></tr><tr><th>7</th><td>C</td><td>48.371736</td><td>V</td><td>101.779140</td></tr><tr><th>8</th><td>D</td><td>-13.473719</td><td>Z</td><td>-25.266714</td></tr><tr><th>9</th><td>E</td><td>37.128002</td><td>Y</td><td>73.118623</td></tr><tr><th>10</th><td>A</td><td>-13.170885</td><td>X</td><td>69.538553</td></tr><tr><th>11</th><td>B</td><td>-13.286488</td><td>Z</td><td>-30.168523</td></tr><tr><th>12</th><td>C</td><td>22.098114</td><td>W</td><td>54.445288</td></tr><tr><th>13</th><td>D</td><td>-85.664012</td><td>W</td><td>-171.324610</td></tr><tr><th>14</th><td>E</td><td>-76.245892</td><td>X</td><td>-48.581133</td></tr><tr><th>15</th><td>A</td><td>-18.114376</td><td>X</td><td>59.816750</td></tr><tr><th>16</th><td>B</td><td>-40.641556</td><td>Z</td><td>-85.182377</td></tr><tr><th>17</th><td>C</td><td>25.712367</td><td>Y</td><td>56.834657</td></tr><tr><th>18</th><td>D</td><td>-35.401204</td><td>Y</td><td>-77.550289</td></tr><tr><th>19</th><td>E</td><td>-60.615185</td><td>Y</td><td>-123.306439</td></tr></tbody></table>

        **Esempio:**

        >>> from cefeste.selection import FeatureSelection
        >>> fs = FeatureSelection(
        ...    db=df_test_filters,
        ...    target_col='target',
        ...    verbose=True # Utile per vedere cosa succede
        ... )
        >>> fs.find_not_explanatory()
        >>> fs.make_report()

        .. raw:: html

            <table border="0" class="jupyter-style-table">  <thead>    <tr style="text-align: right;">      <th></th>      <th>feat_name</th>      <th>result</th>      <th>drop_reason</th>    </tr>  </thead>  <tbody>    <tr>      <th>0</th>      <td>feature_A</td>      <td>drop</td>      <td>unexplanatory</td>    </tr>    <tr>      <th>1</th>      <td>feature_B</td>      <td>keep</td>      <td>NaN</td>    </tr>    <tr>      <th>2</th>      <td>feature_C</td>      <td>keep</td>      <td>NaN</td>    </tr>  </tbody></table>
        """
        self.run(
            filter_constant=False,
            filter_missing=False,
            filter_highly_concentrated=False,
            filter_low_values=False,
            filter_unstable=False,
            filter_unexplanatory=True,
            filter_correlated=False,
            filter_collinear=False,
            **kwargs,
        )
        return

    def find_correlated_features(self, **kwargs):
        """Esegue solo il filtro per le feature altamente correlate.

        Questo metodo è un wrapper attorno al metodo `run`, configurato per attivare specificamente il filtro delle feature altamente correlate e disabilitare tutti gli altri filtri. Aggiorna lo stato dell'istanza in base ai risultati di questo singolo filtro.

        Questa funzione identifica e aiuta a rimuovere le feature altamente correlate. Opera in tre fasi principali, considerando le feature specificate (o tutte se non indicate):

        * Tra **feature numeriche**: Calcola la correlazione (Spearman) tra tutte le possibili coppie di feature numeriche. Se il valore assoluto della correlazione di una coppia supera la soglia (`correlation_threshold`, default 0,95), una delle due feature viene scelta per l'eliminazione. La scelta su quale feature eliminare si basa su una regola (`selection_rule`, default "random"): o casualmente, oppure viene eliminata la feature con potere esplicativo nei confronti della variabile target più basso ("univ_perf"). Questo processo di identificazione ed eliminazione viene ripetuto finché non ci sono più coppie di feature numeriche rimanenti la cui correlazione supera la soglia.
        * Tra **feature categoriche**: Esegue un processo analogo per le coppie di feature categoriche, ma utilizza un'altra misura di associazione (Cramer). Anche qui, se l'associazione supera la soglia, una feature della coppia viene eliminata seguendo la stessa regola di scelta (casuale o potere esplicativo), e il processo è iterativo.
        * Tra **feature miste** (una numerica e una categorica): Calcola una misura di associazione (basata sull'R2 di una regressione fatta sulle colonne dummy categoriche che vanno a prevedere come target la variabile numerica). Se questa misura supera la soglia, una delle due feature della coppia viene eliminata, sempre con la stessa logica di scelta e in modo iterativo.

        Dopo l'applicazione del filtro vengono modificati gli attributi della classe con la selezione effettuata.

        Oltre alla soglia e alla regola di selezione possono essere impostati parametri aggiuntivi come: il seed casuale (`random_state`, default 42), il dataset contenente il potere esplicativo di ciascuna feature sul target (`feat_univ_perf`, default `DataFrame` vuoto), la richiesta di avere più dettagli in output (`verbose`, default `False`), la richiesta di avere le scelte di selezione (`return_selection_history`, default `False`) e la richiesta di avere un dataset addizionale contenente le correlazioni medie tra feature (`return_avg_correlation`, default `False`).

        Args:
            **kwargs: Argomenti keyword aggiuntivi per sovrascrivere i parametri dell'istanza per questa esecuzione.

        **Dati utilizzati per gli esempi:**

            >>> db_test_filters

            .. raw:: html

                <style>
                   /* Stile base per la tabella con la nostra classe specifica */
                   .jupyter-style-table {
                       border-collapse: collapse; /* Bordi uniti */
                       margin: 1em 0; /* Margine sopra/sotto */
                       font-family: "Helvetica Neue", Helvetica, Arial, sans-serif; /* Font simile a Jupyter */
                       font-size: 0.9em; /* Dimensione font leggermente ridotta */
                       border: 1px solid #d3d3d3; /* Bordo esterno leggero */
                       width: auto; /* Larghezza basata sul contenuto */
                       max-width: 100%; /* Non superare il contenitore */
                       overflow-x: auto; /* Abilita lo scroll orizzontale se necessario (meglio sul wrapper, ma ok qui) */
                       display: block; /* Necessario per far funzionare overflow-x su una tabella */
                   }

                   /* Stile per le celle dell'header (th) */
                   .jupyter-style-table thead th {
                       background-color: #f5f5f5; /* Sfondo grigio chiaro per header */
                       font-weight: bold; /* Grassetto */
                       padding: 8px 10px; /* Padding interno */
                       text-align: right; /* Allineamento testo (spesso a destra per numeri/default) */
                       border-bottom: 1px solid #d3d3d3; /* Linea sotto l'header */
                       vertical-align: bottom; /* Allineamento verticale */
                   }

                   /* Stile per le celle dei dati (td) */
                   .jupyter-style-table tbody td {
                       padding: 6px 10px; /* Padding interno */
                       text-align: right; /* Allineamento testo (aggiusta se hai testo a sinistra) */
                       border-right: 1px solid #d3d3d3; /* Linea verticale tra celle (opzionale) */
                       border-top: 1px solid #d3d3d3; /* Linea orizzontale tra righe */
                       vertical-align: middle; /* Allineamento verticale */
                   }
                   .jupyter-style-table tbody td:last-child {
                       border-right: none; /* Rimuovi bordo destro sull'ultima cella */
                   }

                   /* Stile per l'header dell'indice (se presente) */
                   .jupyter-style-table thead th.blank { /* Header vuoto sopra l'indice */
                       background-color: white;
                       border: none;
                   }
                   .jupyter-style-table tbody th { /* Celle dell'indice nel body */
                       padding: 6px 10px;
                       text-align: right;
                       font-weight: normal;
                       border-right: 1px solid #d3d3d3;
                       border-top: 1px solid #d3d3d3;
                       background-color: #f5f5f5; /* Sfondo leggero per indice */
                   }


                   /* Striping delle righe (alternanza colori) */
                   .jupyter-style-table tbody tr:nth-child(even) {
                       background-color: #f9f9f9; /* Sfondo molto leggero per righe pari */
                   }

                   /* Effetto Hover (cambio colore al passaggio del mouse) */
                   .jupyter-style-table tbody tr:hover {
                       background-color: #f0f0f0; /* Sfondo leggermente più scuro su hover */
                   }
                </style>
                <table border="0" class="jupyter-style-table"><thead><tr style="text-align: right;"><th></th><th>feature_B</th><th>feature_C</th><th>feature_A1</th><th>feature_A2</th></tr></thead><tbody><tr><th>0</th><td>34.835708</td><td>Z</td><td>-0.270712</td><td>-0.812137</td></tr><tr><th>1</th><td>3.086785</td><td>X</td><td>0.104848</td><td>0.314544</td></tr><tr><th>2</th><td>42.384427</td><td>Y</td><td>0.250528</td><td>0.751583</td></tr><tr><th>3</th><td>86.151493</td><td>X</td><td>-0.925200</td><td>-2.775600</td></tr><tr><th>4</th><td>-1.707669</td><td>V</td><td>0.567144</td><td>1.701431</td></tr><tr><th>5</th><td>-1.706848</td><td>V</td><td>-1.040180</td><td>-3.120541</td></tr><tr><th>6</th><td>88.960641</td><td>X</td><td>-0.153676</td><td>-0.461028</td></tr><tr><th>7</th><td>48.371736</td><td>V</td><td>0.789852</td><td>2.369555</td></tr><tr><th>8</th><td>-13.473719</td><td>Z</td><td>-1.226216</td><td>-3.678648</td></tr><tr><th>9</th><td>37.128002</td><td>Y</td><td>-0.948007</td><td>-2.844021</td></tr><tr><th>10</th><td>-13.170885</td><td>X</td><td>-0.569654</td><td>-1.708962</td></tr><tr><th>11</th><td>-13.286488</td><td>Z</td><td>-0.977150</td><td>-2.931451</td></tr><tr><th>12</th><td>22.098114</td><td>W</td><td>-0.770632</td><td>-2.311895</td></tr><tr><th>13</th><td>-85.664012</td><td>W</td><td>-0.033711</td><td>-0.101134</td></tr><tr><th>14</th><td>-76.245892</td><td>X</td><td>-1.032859</td><td>-3.098578</td></tr><tr><th>15</th><td>-18.114376</td><td>X</td><td>1.142427</td><td>3.427282</td></tr><tr><th>16</th><td>-40.641556</td><td>Z</td><td>-0.609778</td><td>-1.829334</td></tr><tr><th>17</th><td>25.712367</td><td>Y</td><td>1.469416</td><td>4.408249</td></tr><tr><th>18</th><td>-35.401204</td><td>Y</td><td>1.492679</td><td>4.478037</td></tr><tr><th>19</th><td>-60.615185</td><td>Y</td><td>0.707125</td><td>2.121376</td></tr></tbody></table>

        **Esempio:**

        >>> from cefeste.selection import FeatureSelection
        >>> fs = FeatureSelection(
        ...    db=df_test_filters,
        ...    verbose=True # Utile per vedere cosa succede
        ... )
        >>> fs.find_correlated_features()
        >>> fs.make_report()

        .. raw:: html

            <table border="0" class="jupyter-style-table">  <thead>    <tr style="text-align: right;">      <th></th>      <th>feat_name</th>      <th>result</th>      <th>drop_reason</th>    </tr>  </thead>  <tbody>    <tr>      <th>0</th>      <td>feature_A2</td>      <td>drop</td>      <td>correlated</td>    </tr>    <tr>      <th>1</th>      <td>feature_A1</td>      <td>keep</td>      <td>NaN</td>    </tr>    <tr>      <th>2</th>      <td>feature_C</td>      <td>keep</td>      <td>NaN</td>    </tr>    <tr>      <th>3</th>      <td>feature_B</td>      <td>keep</td>      <td>NaN</td>    </tr>  </tbody></table>
        """
        self.run(
            filter_constant=False,
            filter_missing=False,
            filter_highly_concentrated=False,
            filter_low_values=False,
            filter_unstable=False,
            filter_unexplanatory=False,
            filter_correlated=True,
            filter_collinear=False,
            **kwargs,
        )
        return

    def find_collinear_feature_optimized(self, **kwargs):
        """Esegue solo il filtro per le feature collineari (basato su VIF).

        Questo metodo è un wrapper attorno al metodo `run`, configurato per attivare specificamente il filtro delle feature collineari e disabilitare tutti gli altri filtri. Aggiorna lo stato dell'istanza in base ai risultati di questo singolo filtro.

        Questa funzione ha lo scopo di identificare e suggerire la rimozione di feature numeriche che causano multicollinearità, basandosi sul calcolo del VIF (Variance Inflation Factor). Può operare in due modi distinti, a seconda che si attivi o meno un'opzione di ottimizzazione:

        * **Modalità non ottimizzata** (quando il parametro `optimize` è `False`, default): In questa modalità, la funzione inizia analizzando le feature numeriche del `DataFrame`, o un sottoinsieme da te specificato. Per queste feature, calcola il Variance Inflation Factor (VIF). Successivamente, individua la feature che presenta il valore di VIF più elevato. Se questo VIF massimo supera una certa soglia (`vif_threshold`, default 5), quella feature viene considerata problematica e viene virtualmente rimossa. Il processo viene quindi ripetuto: sui dati rimanenti (senza la feature appena eliminata) si ricalcolano i VIF, si identifica nuovamente la feature con il VIF più alto e si confronta con la soglia. Questo ciclo iterativo di calcolo, identificazione e rimozione prosegue finché i VIF di tutte le feature numeriche ancora in gioco non risultano inferiori alla soglia stabilita.
        * **Modalità ottimizzata** (quando il parametro `optimize` è `True`): Quando si attiva questa modalità, la funzione adotta un approccio differente, sempre concentrandosi sulle feature numeriche. Le feature vengono esaminate seguendo un ordine preciso, che deve fornire l'utente attraverso un parametro specifico (`optim_Series`,ovvero una `pd.Series`, default `None`), il quale determina la sequenza di controllo (se `None` non viene eliminata alcuna feature, anche se collineare). La funzione scorre le feature una ad una, rispettando rigorosamente questo ordine prestabilito. Per ogni feature, nel momento in cui viene analizzata secondo la sequenza, si calcola il suo VIF (considerando solo le feature che non sono state eliminate nei passaggi precedenti dell'analisi). Se il VIF di quella specifica feature, al momento del suo controllo, risulta superiore alla soglia, allora quella feature viene identificata per la rimozione. Indipendentemente dal fatto che la feature corrente sia stata rimossa o meno, la funzione procede poi a esaminare la feature successiva nell'ordine definito.

        Dopo l'applicazione del filtro vengono modificati gli attributi della classe con la selezione effettuata.

        Oltre alla soglia, all'opzione di ottimizzazione e alla sequenza di analisi possono essere impostati parametri aggiuntivi come: la richiesta di avere più dettagli in output (`verbose`, default `False`) e l'ordine crescente (in base al valore del VIF) di analisi, ovvero analizzare per prima la feature con il valore più basso (`optim_value_ascending`, default `True`).

        Args:
            **kwargs: Argomenti keyword aggiuntivi per sovrascrivere i parametri dell'istanza per questa esecuzione.

        **Dati utilizzati per gli esempi:**

            >>> db_test_filters

            .. raw:: html

                <style>
                   /* Stile base per la tabella con la nostra classe specifica */
                   .jupyter-style-table {
                       border-collapse: collapse; /* Bordi uniti */
                       margin: 1em 0; /* Margine sopra/sotto */
                       font-family: "Helvetica Neue", Helvetica, Arial, sans-serif; /* Font simile a Jupyter */
                       font-size: 0.9em; /* Dimensione font leggermente ridotta */
                       border: 1px solid #d3d3d3; /* Bordo esterno leggero */
                       width: auto; /* Larghezza basata sul contenuto */
                       max-width: 100%; /* Non superare il contenitore */
                       overflow-x: auto; /* Abilita lo scroll orizzontale se necessario (meglio sul wrapper, ma ok qui) */
                       display: block; /* Necessario per far funzionare overflow-x su una tabella */
                   }

                   /* Stile per le celle dell'header (th) */
                   .jupyter-style-table thead th {
                       background-color: #f5f5f5; /* Sfondo grigio chiaro per header */
                       font-weight: bold; /* Grassetto */
                       padding: 8px 10px; /* Padding interno */
                       text-align: right; /* Allineamento testo (spesso a destra per numeri/default) */
                       border-bottom: 1px solid #d3d3d3; /* Linea sotto l'header */
                       vertical-align: bottom; /* Allineamento verticale */
                   }

                   /* Stile per le celle dei dati (td) */
                   .jupyter-style-table tbody td {
                       padding: 6px 10px; /* Padding interno */
                       text-align: right; /* Allineamento testo (aggiusta se hai testo a sinistra) */
                       border-right: 1px solid #d3d3d3; /* Linea verticale tra celle (opzionale) */
                       border-top: 1px solid #d3d3d3; /* Linea orizzontale tra righe */
                       vertical-align: middle; /* Allineamento verticale */
                   }
                   .jupyter-style-table tbody td:last-child {
                       border-right: none; /* Rimuovi bordo destro sull'ultima cella */
                   }

                   /* Stile per l'header dell'indice (se presente) */
                   .jupyter-style-table thead th.blank { /* Header vuoto sopra l'indice */
                       background-color: white;
                       border: none;
                   }
                   .jupyter-style-table tbody th { /* Celle dell'indice nel body */
                       padding: 6px 10px;
                       text-align: right;
                       font-weight: normal;
                       border-right: 1px solid #d3d3d3;
                       border-top: 1px solid #d3d3d3;
                       background-color: #f5f5f5; /* Sfondo leggero per indice */
                   }


                   /* Striping delle righe (alternanza colori) */
                   .jupyter-style-table tbody tr:nth-child(even) {
                       background-color: #f9f9f9; /* Sfondo molto leggero per righe pari */
                   }

                   /* Effetto Hover (cambio colore al passaggio del mouse) */
                   .jupyter-style-table tbody tr:hover {
                       background-color: #f0f0f0; /* Sfondo leggermente più scuro su hover */
                   }
                </style>
                <table border="0" class="jupyter-style-table"><thead><tr style="text-align: right;"><th></th><th>feature_B</th><th>feature_C</th><th>feature_A1</th><th>feature_A2</th><th>feature_A3</th></tr></thead><tbody><tr><th>0</th><td>34.835708</td><td>Z</td><td>-0.270712</td><td>-0.607548</td><td>-0.878260</td></tr><tr><th>1</th><td>3.086785</td><td>X</td><td>0.104848</td><td>-0.126136</td><td>-0.021288</td></tr><tr><th>2</th><td>42.384427</td><td>Y</td><td>0.250528</td><td>-0.684606</td><td>-0.434079</td></tr><tr><th>3</th><td>86.151493</td><td>X</td><td>-0.925200</td><td>0.928715</td><td>0.003515</td></tr><tr><th>4</th><td>-1.707669</td><td>V</td><td>0.567144</td><td>-1.844401</td><td>-1.277257</td></tr><tr><th>5</th><td>-1.706848</td><td>V</td><td>-1.040180</td><td>-0.467002</td><td>-1.507183</td></tr><tr><th>6</th><td>88.960641</td><td>X</td><td>-0.153676</td><td>2.292490</td><td>2.138814</td></tr><tr><th>7</th><td>48.371736</td><td>V</td><td>0.789852</td><td>0.488810</td><td>1.278662</td></tr><tr><th>8</th><td>-13.473719</td><td>Z</td><td>-1.226216</td><td>0.710267</td><td>-0.515949</td></tr><tr><th>9</th><td>37.128002</td><td>Y</td><td>-0.948007</td><td>1.055534</td><td>0.107527</td></tr><tr><th>10</th><td>-13.170885</td><td>X</td><td>-0.569654</td><td>0.054073</td><td>-0.515581</td></tr><tr><th>11</th><td>-13.286488</td><td>Z</td><td>-0.977150</td><td>0.257953</td><td>-0.719197</td></tr><tr><th>12</th><td>22.098114</td><td>W</td><td>-0.770632</td><td>0.588282</td><td>-0.182350</td></tr><tr><th>13</th><td>-85.664012</td><td>W</td><td>-0.033711</td><td>0.885244</td><td>0.851533</td></tr><tr><th>14</th><td>-76.245892</td><td>X</td><td>-1.032859</td><td>-1.017007</td><td>-2.049866</td></tr><tr><th>15</th><td>-18.114376</td><td>X</td><td>1.142427</td><td>-0.133693</td><td>1.008734</td></tr><tr><th>16</th><td>-40.641556</td><td>Z</td><td>-0.609778</td><td>-0.438186</td><td>-1.047964</td></tr><tr><th>17</th><td>25.712367</td><td>Y</td><td>1.469416</td><td>0.493443</td><td>1.962860</td></tr><tr><th>18</th><td>-35.401204</td><td>Y</td><td>1.492679</td><td>-0.199009</td><td>1.293670</td></tr><tr><th>19</th><td>-60.615185</td><td>Y</td><td>0.707125</td><td>-1.274984</td><td>-0.567858</td></tr></tbody></table>

        **Esempio:**

        >>> from cefeste.selection import FeatureSelection
        >>> fs = FeatureSelection(
        ...    db=df_test_filters,
        ...    verbose=True # Utile per vedere cosa succede
        ... )
        >>> fs.find_collinear_feature_optimized()
        >>> fs.make_report()

        .. raw:: html

            <table border="0" class="jupyter-style-table">  <thead>    <tr style="text-align: right;">      <th></th>      <th>feat_name</th>      <th>result</th>      <th>drop_reason</th>    </tr>  </thead>  <tbody>    <tr>      <th>0</th>      <td>feature_A3</td>      <td>drop</td>      <td>collinear</td>    </tr>    <tr>      <th>1</th>      <td>feature_A1</td>      <td>keep</td>      <td>NaN</td>    </tr>    <tr>      <th>2</th>      <td>feature_A2</td>      <td>keep</td>      <td>NaN</td>    </tr>    <tr>      <th>3</th>      <td>feature_C</td>      <td>keep</td>      <td>NaN</td>    </tr>    <tr>      <th>4</th>      <td>feature_B</td>      <td>keep</td>      <td>NaN</td>    </tr>  </tbody></table>
        """
        self.run(
            filter_constant=False,
            filter_missing=False,
            filter_highly_concentrated=False,
            filter_low_values=False,
            filter_unstable=False,
            filter_unexplanatory=False,
            filter_correlated=False,
            filter_collinear=True,
            **kwargs,
        )
        return

    def get_X_original(self):
        """Restituisce il `DataFrame` originale contenente solo le feature inizialmente considerate.

        Seleziona dal `DataFrame` originale (attributo `db`) solo le colonne presenti nell'attributo `feat_to_check`, ovvero le feature che sono state incluse all'inizio del processo di analisi/selezione.

        Returns:
            `pd.DataFrame`: Un `DataFrame` contenente solo le colonne specificate in `feat_to_check`.

        **Dati utilizzati per gli esempi:**

        >>> db_test_filters

            .. raw:: html

                <style>
                   /* Stile base per la tabella con la nostra classe specifica */
                   .jupyter-style-table {
                       border-collapse: collapse; /* Bordi uniti */
                       margin: 1em 0; /* Margine sopra/sotto */
                       font-family: "Helvetica Neue", Helvetica, Arial, sans-serif; /* Font simile a Jupyter */
                       font-size: 0.9em; /* Dimensione font leggermente ridotta */
                       border: 1px solid #d3d3d3; /* Bordo esterno leggero */
                       width: auto; /* Larghezza basata sul contenuto */
                       max-width: 100%; /* Non superare il contenitore */
                       overflow-x: auto; /* Abilita lo scroll orizzontale se necessario (meglio sul wrapper, ma ok qui) */
                       display: block; /* Necessario per far funzionare overflow-x su una tabella */
                   }

                   /* Stile per le celle dell'header (th) */
                   .jupyter-style-table thead th {
                       background-color: #f5f5f5; /* Sfondo grigio chiaro per header */
                       font-weight: bold; /* Grassetto */
                       padding: 8px 10px; /* Padding interno */
                       text-align: right; /* Allineamento testo (spesso a destra per numeri/default) */
                       border-bottom: 1px solid #d3d3d3; /* Linea sotto l'header */
                       vertical-align: bottom; /* Allineamento verticale */
                   }

                   /* Stile per le celle dei dati (td) */
                   .jupyter-style-table tbody td {
                       padding: 6px 10px; /* Padding interno */
                       text-align: right; /* Allineamento testo (aggiusta se hai testo a sinistra) */
                       border-right: 1px solid #d3d3d3; /* Linea verticale tra celle (opzionale) */
                       border-top: 1px solid #d3d3d3; /* Linea orizzontale tra righe */
                       vertical-align: middle; /* Allineamento verticale */
                   }
                   .jupyter-style-table tbody td:last-child {
                       border-right: none; /* Rimuovi bordo destro sull'ultima cella */
                   }

                   /* Stile per l'header dell'indice (se presente) */
                   .jupyter-style-table thead th.blank { /* Header vuoto sopra l'indice */
                       background-color: white;
                       border: none;
                   }
                   .jupyter-style-table tbody th { /* Celle dell'indice nel body */
                       padding: 6px 10px;
                       text-align: right;
                       font-weight: normal;
                       border-right: 1px solid #d3d3d3;
                       border-top: 1px solid #d3d3d3;
                       background-color: #f5f5f5; /* Sfondo leggero per indice */
                   }


                   /* Striping delle righe (alternanza colori) */
                   .jupyter-style-table tbody tr:nth-child(even) {
                       background-color: #f9f9f9; /* Sfondo molto leggero per righe pari */
                   }

                   /* Effetto Hover (cambio colore al passaggio del mouse) */
                   .jupyter-style-table tbody tr:hover {
                       background-color: #f0f0f0; /* Sfondo leggermente più scuro su hover */
                   }
                </style>
                <table border="0" class="jupyter-style-table"><thead><tr style="text-align: right;"><th></th><th>feature_B</th><th>feature_C</th><th>feature_A1</th><th>feature_A2</th></tr></thead><tbody><tr><th>0</th><td>34.835708</td><td>Z</td><td>-0.270712</td><td>-0.812137</td></tr><tr><th>1</th><td>3.086785</td><td>X</td><td>0.104848</td><td>0.314544</td></tr><tr><th>2</th><td>42.384427</td><td>Y</td><td>0.250528</td><td>0.751583</td></tr><tr><th>3</th><td>86.151493</td><td>X</td><td>-0.925200</td><td>-2.775600</td></tr><tr><th>4</th><td>-1.707669</td><td>V</td><td>0.567144</td><td>1.701431</td></tr><tr><th>5</th><td>-1.706848</td><td>V</td><td>-1.040180</td><td>-3.120541</td></tr><tr><th>6</th><td>88.960641</td><td>X</td><td>-0.153676</td><td>-0.461028</td></tr><tr><th>7</th><td>48.371736</td><td>V</td><td>0.789852</td><td>2.369555</td></tr><tr><th>8</th><td>-13.473719</td><td>Z</td><td>-1.226216</td><td>-3.678648</td></tr><tr><th>9</th><td>37.128002</td><td>Y</td><td>-0.948007</td><td>-2.844021</td></tr><tr><th>10</th><td>-13.170885</td><td>X</td><td>-0.569654</td><td>-1.708962</td></tr><tr><th>11</th><td>-13.286488</td><td>Z</td><td>-0.977150</td><td>-2.931451</td></tr><tr><th>12</th><td>22.098114</td><td>W</td><td>-0.770632</td><td>-2.311895</td></tr><tr><th>13</th><td>-85.664012</td><td>W</td><td>-0.033711</td><td>-0.101134</td></tr><tr><th>14</th><td>-76.245892</td><td>X</td><td>-1.032859</td><td>-3.098578</td></tr><tr><th>15</th><td>-18.114376</td><td>X</td><td>1.142427</td><td>3.427282</td></tr><tr><th>16</th><td>-40.641556</td><td>Z</td><td>-0.609778</td><td>-1.829334</td></tr><tr><th>17</th><td>25.712367</td><td>Y</td><td>1.469416</td><td>4.408249</td></tr><tr><th>18</th><td>-35.401204</td><td>Y</td><td>1.492679</td><td>4.478037</td></tr><tr><th>19</th><td>-60.615185</td><td>Y</td><td>0.707125</td><td>2.121376</td></tr></tbody></table>

        **Esempio:**

        >>> from cefeste.selection import FeatureSelection
        >>> fs = FeatureSelection(
        ...    db=df_test_filters,
        ...    verbose=True # Utile per vedere cosa succede
        ... )
        >>> fs.find_correlated_features()
        >>> fs.make_report()

        .. raw:: html

            <table border="0" class="jupyter-style-table">  <thead>    <tr style="text-align: right;">      <th></th>      <th>feat_name</th>      <th>result</th>      <th>drop_reason</th>    </tr>  </thead>  <tbody>    <tr>      <th>0</th>      <td>feature_A2</td>      <td>drop</td>      <td>correlated</td>    </tr>    <tr>      <th>1</th>      <td>feature_A1</td>      <td>keep</td>      <td>NaN</td>    </tr>    <tr>      <th>2</th>      <td>feature_C</td>      <td>keep</td>      <td>NaN</td>    </tr>    <tr>      <th>3</th>      <td>feature_B</td>      <td>keep</td>      <td>NaN</td>    </tr>  </tbody></table>

        >>> fs.get_X_original()

        .. raw:: html

            <table border="0" class="jupyter-style-table"><thead><tr style="text-align: right;"><th></th><th>feature_B</th><th>feature_C</th><th>feature_A1</th><th>feature_A2</th></tr></thead><tbody><tr><th>0</th><td>34.835708</td><td>Z</td><td>-0.270712</td><td>-0.812137</td></tr><tr><th>1</th><td>3.086785</td><td>X</td><td>0.104848</td><td>0.314544</td></tr><tr><th>2</th><td>42.384427</td><td>Y</td><td>0.250528</td><td>0.751583</td></tr><tr><th>3</th><td>86.151493</td><td>X</td><td>-0.925200</td><td>-2.775600</td></tr><tr><th>4</th><td>-1.707669</td><td>V</td><td>0.567144</td><td>1.701431</td></tr><tr><th>5</th><td>-1.706848</td><td>V</td><td>-1.040180</td><td>-3.120541</td></tr><tr><th>6</th><td>88.960641</td><td>X</td><td>-0.153676</td><td>-0.461028</td></tr><tr><th>7</th><td>48.371736</td><td>V</td><td>0.789852</td><td>2.369555</td></tr><tr><th>8</th><td>-13.473719</td><td>Z</td><td>-1.226216</td><td>-3.678648</td></tr><tr><th>9</th><td>37.128002</td><td>Y</td><td>-0.948007</td><td>-2.844021</td></tr><tr><th>10</th><td>-13.170885</td><td>X</td><td>-0.569654</td><td>-1.708962</td></tr><tr><th>11</th><td>-13.286488</td><td>Z</td><td>-0.977150</td><td>-2.931451</td></tr><tr><th>12</th><td>22.098114</td><td>W</td><td>-0.770632</td><td>-2.311895</td></tr><tr><th>13</th><td>-85.664012</td><td>W</td><td>-0.033711</td><td>-0.101134</td></tr><tr><th>14</th><td>-76.245892</td><td>X</td><td>-1.032859</td><td>-3.098578</td></tr><tr><th>15</th><td>-18.114376</td><td>X</td><td>1.142427</td><td>3.427282</td></tr><tr><th>16</th><td>-40.641556</td><td>Z</td><td>-0.609778</td><td>-1.829334</td></tr><tr><th>17</th><td>25.712367</td><td>Y</td><td>1.469416</td><td>4.408249</td></tr><tr><th>18</th><td>-35.401204</td><td>Y</td><td>1.492679</td><td>4.478037</td></tr><tr><th>19</th><td>-60.615185</td><td>Y</td><td>0.707125</td><td>2.121376</td></tr></tbody></table>
        """
        return self.db[self.feat_to_check]

    def get_X_reduced(self):
        """Restituisce il `DataFrame` contenente solo le feature finali selezionate.

        Seleziona dal `DataFrame` originale (attributo `db`) solo le colonne presenti nell'attributo `final_feat`, che è stata popolata dalla fase di selezione. Questo rappresenta il set di feature dopo la feature selection.

        Returns:
            `pd.DataFrame`: Un `DataFrame` contenente solo le colonne delle feature finali selezionate.

        Note:
            Assicurarsi di aver eseguito i metodi dei filtri desiderati prima di chiamare questo metodo per ottenere un risultato significativo.

        **Dati utilizzati per gli esempi:**

        >>> df_test_filters

        .. raw:: html

            <style>
                   /* Stile base per la tabella con la nostra classe specifica */
                   .jupyter-style-table {
                       border-collapse: collapse; /* Bordi uniti */
                       margin: 1em 0; /* Margine sopra/sotto */
                       font-family: "Helvetica Neue", Helvetica, Arial, sans-serif; /* Font simile a Jupyter */
                       font-size: 0.9em; /* Dimensione font leggermente ridotta */
                       border: 1px solid #d3d3d3; /* Bordo esterno leggero */
                       width: auto; /* Larghezza basata sul contenuto */
                       max-width: 100%; /* Non superare il contenitore */
                       overflow-x: auto; /* Abilita lo scroll orizzontale se necessario (meglio sul wrapper, ma ok qui) */
                       display: block; /* Necessario per far funzionare overflow-x su una tabella */
                   }

                   /* Stile per le celle dell'header (th) */
                   .jupyter-style-table thead th {
                       background-color: #f5f5f5; /* Sfondo grigio chiaro per header */
                       font-weight: bold; /* Grassetto */
                       padding: 8px 10px; /* Padding interno */
                       text-align: right; /* Allineamento testo (spesso a destra per numeri/default) */
                       border-bottom: 1px solid #d3d3d3; /* Linea sotto l'header */
                       vertical-align: bottom; /* Allineamento verticale */
                   }

                   /* Stile per le celle dei dati (td) */
                   .jupyter-style-table tbody td {
                       padding: 6px 10px; /* Padding interno */
                       text-align: right; /* Allineamento testo (aggiusta se hai testo a sinistra) */
                       border-right: 1px solid #d3d3d3; /* Linea verticale tra celle (opzionale) */
                       border-top: 1px solid #d3d3d3; /* Linea orizzontale tra righe */
                       vertical-align: middle; /* Allineamento verticale */
                   }
                   .jupyter-style-table tbody td:last-child {
                       border-right: none; /* Rimuovi bordo destro sull'ultima cella */
                   }

                   /* Stile per l'header dell'indice (se presente) */
                   .jupyter-style-table thead th.blank { /* Header vuoto sopra l'indice */
                       background-color: white;
                       border: none;
                   }
                   .jupyter-style-table tbody th { /* Celle dell'indice nel body */
                       padding: 6px 10px;
                       text-align: right;
                       font-weight: normal;
                       border-right: 1px solid #d3d3d3;
                       border-top: 1px solid #d3d3d3;
                       background-color: #f5f5f5; /* Sfondo leggero per indice */
                   }


                   /* Striping delle righe (alternanza colori) */
                   .jupyter-style-table tbody tr:nth-child(even) {
                       background-color: #f9f9f9; /* Sfondo molto leggero per righe pari */
                   }

                   /* Effetto Hover (cambio colore al passaggio del mouse) */
                   .jupyter-style-table tbody tr:hover {
                       background-color: #f0f0f0; /* Sfondo leggermente più scuro su hover */
                   }
                </style>
                <table border="0" class="jupyter-style-table">  <thead>    <tr style="text-align: right;">      <th></th>      <th>feature_B</th>      <th>feature_C</th>      <th>target</th>      <th>feature_A1</th>      <th>feature_A2</th>      <th>sample_col</th>    </tr>  </thead>  <tbody>    <tr>      <th>0</th>      <td>34.835708</td>      <td>Z</td>      <td>75.013312</td>      <td>-0.270712</td>      <td>-0.812137</td>      <td>train</td>    </tr>    <tr>      <th>1</th>      <td>3.086785</td>      <td>X</td>      <td>109.194174</td>      <td>0.104848</td>      <td>0.314544</td>      <td>train</td>    </tr>    <tr>      <th>2</th>      <td>42.384427</td>      <td>Y</td>      <td>96.287048</td>      <td>0.250528</td>      <td>0.751583</td>      <td>train</td>    </tr>    <tr>      <th>3</th>      <td>86.151493</td>      <td>X</td>      <td>264.905765</td>      <td>-0.925200</td>      <td>-2.775600</td>      <td>train</td>    </tr>    <tr>      <th>4</th>      <td>-1.707669</td>      <td>V</td>      <td>2.880829</td>      <td>0.567144</td>      <td>1.701431</td>      <td>train</td>    </tr>    <tr>      <th>5</th>      <td>-1.706848</td>      <td>V</td>      <td>2.318509</td>      <td>-1.040180</td>      <td>-3.120541</td>      <td>train</td>    </tr>    <tr>      <th>6</th>      <td>88.960641</td>      <td>X</td>      <td>273.054387</td>      <td>-0.153676</td>      <td>-0.461028</td>      <td>train</td>    </tr>    <tr>      <th>7</th>      <td>48.371736</td>      <td>V</td>      <td>101.779140</td>      <td>0.789852</td>      <td>2.369555</td>      <td>train</td>    </tr>    <tr>      <th>8</th>      <td>-13.473719</td>      <td>Z</td>      <td>-25.266714</td>      <td>-1.226216</td>      <td>-3.678648</td>      <td>train</td>    </tr>    <tr>      <th>9</th>      <td>37.128002</td>      <td>Y</td>      <td>73.118623</td>      <td>-0.948007</td>      <td>-2.844021</td>      <td>train</td>    </tr>    <tr>      <th>10</th>      <td>-13.170885</td>      <td>X</td>      <td>69.538553</td>      <td>-0.569654</td>      <td>-1.708962</td>      <td>train</td>    </tr>    <tr>      <th>11</th>      <td>-13.286488</td>      <td>Z</td>      <td>-30.168523</td>      <td>-0.977150</td>      <td>-2.931451</td>      <td>train</td>    </tr>    <tr>      <th>12</th>      <td>22.098114</td>      <td>W</td>      <td>54.445288</td>      <td>-0.770632</td>      <td>-2.311895</td>      <td>train</td>    </tr>    <tr>      <th>13</th>      <td>-85.664012</td>      <td>W</td>      <td>-171.324610</td>      <td>-0.033711</td>      <td>-0.101134</td>      <td>train</td>    </tr>    <tr>      <th>14</th>      <td>-76.245892</td>      <td>X</td>      <td>-48.581133</td>      <td>-1.032859</td>      <td>-3.098578</td>      <td>train</td>    </tr>    <tr>      <th>15</th>      <td>-18.114376</td>      <td>X</td>      <td>59.816750</td>      <td>1.142427</td>      <td>3.427282</td>      <td>train</td>    </tr>    <tr>      <th>16</th>      <td>-40.641556</td>      <td>Z</td>      <td>-85.182377</td>      <td>-0.609778</td>      <td>-1.829334</td>      <td>train</td>    </tr>    <tr>      <th>17</th>      <td>25.712367</td>      <td>Y</td>      <td>56.834657</td>      <td>1.469416</td>      <td>4.408249</td>      <td>train</td>    </tr>    <tr>      <th>18</th>      <td>-35.401204</td>      <td>Y</td>      <td>-77.550289</td>      <td>1.492679</td>      <td>4.478037</td>      <td>train</td>    </tr>    <tr>      <th>19</th>      <td>-60.615185</td>      <td>Y</td>      <td>-123.306439</td>      <td>0.707125</td>      <td>2.121376</td>      <td>train</td>    </tr>  </tbody></table>

        **Esempio:**

        >>> from cefeste.selection import FeatureSelection
        >>> fs = FeatureSelection(
        ...  db=df_test_filters,
        ...  target_col='target',
        ...  sample_col='sample_col',
        ...  sample_train_value='train',
        ...  verbose=True
        ... )
        >>> fs.run()
        >>> fs.make_report()

        .. raw:: html

            <table border="0" class="jupyter-style-table">  <thead>    <tr style="text-align: right;">      <th></th>      <th>feat_name</th>      <th>result</th>      <th>drop_reason</th>    </tr>  </thead>  <tbody>    <tr>      <th>0</th>      <td>feature_A1</td>      <td>drop</td>      <td>unexplanatory</td>    </tr>    <tr>      <th>1</th>      <td>feature_A2</td>      <td>drop</td>      <td>unexplanatory</td>    </tr>    <tr>      <th>2</th>      <td>feature_C</td>      <td>keep</td>      <td>NaN</td>    </tr>    <tr>      <th>3</th>      <td>feature_B</td>      <td>keep</td>      <td>NaN</td>    </tr>  </tbody></table>

        >>> fs.get_X_reduced()

        .. raw:: html

            <table border="0" class="jupyter-style-table">  <thead>    <tr style="text-align: right;">      <th></th>      <th>feature_C</th>      <th>feature_B</th>    </tr>  </thead>  <tbody>    <tr>      <th>0</th>      <td>Z</td>      <td>34.835708</td>    </tr>    <tr>      <th>1</th>      <td>X</td>      <td>3.086785</td>    </tr>    <tr>      <th>2</th>      <td>Y</td>      <td>42.384427</td>    </tr>    <tr>      <th>3</th>      <td>X</td>      <td>86.151493</td>    </tr>    <tr>      <th>4</th>      <td>V</td>      <td>-1.707669</td>    </tr>    <tr>      <th>5</th>      <td>V</td>      <td>-1.706848</td>    </tr>    <tr>      <th>6</th>      <td>X</td>      <td>88.960641</td>    </tr>    <tr>      <th>7</th>      <td>V</td>      <td>48.371736</td>    </tr>    <tr>      <th>8</th>      <td>Z</td>      <td>-13.473719</td>    </tr>    <tr>      <th>9</th>      <td>Y</td>      <td>37.128002</td>    </tr>    <tr>      <th>10</th>      <td>X</td>      <td>-13.170885</td>    </tr>    <tr>      <th>11</th>      <td>Z</td>      <td>-13.286488</td>    </tr>    <tr>      <th>12</th>      <td>W</td>      <td>22.098114</td>    </tr>    <tr>      <th>13</th>      <td>W</td>      <td>-85.664012</td>    </tr>    <tr>      <th>14</th>      <td>X</td>      <td>-76.245892</td>    </tr>    <tr>      <th>15</th>      <td>X</td>      <td>-18.114376</td>    </tr>    <tr>      <th>16</th>      <td>Z</td>      <td>-40.641556</td>    </tr>    <tr>      <th>17</th>      <td>Y</td>      <td>25.712367</td>    </tr>    <tr>      <th>18</th>      <td>Y</td>      <td>-35.401204</td>    </tr>    <tr>      <th>19</th>      <td>Y</td>      <td>-60.615185</td>    </tr>  </tbody></table>
        """
        return self.db[self._selected_features]

    def get_db_filtered(self):
        """Restituisce il `DataFrame` originale senza le feature eliminate.

        Rimuove dal `DataFrame` originale (attributo `db`) le colonne corrispondenti alle feature che sono state memorizzate nell'attributo `_filtered_out_features` dai vari filtri di selezione. Mantiene tutte le altre colonne originali (inclusi target, sample_col, ecc.). Questo rappresenta il dataset dopo l'applicazione dei filtri della feature selection.

        Returns:
            `pd.DataFrame`: Il `DataFrame` originale con le colonne delle feature eliminate rimosse.

        **Dati utilizzati per gli esempi:**

        >>> df_test_filters

        .. raw:: html

            <style>
                   /* Stile base per la tabella con la nostra classe specifica */
                   .jupyter-style-table {
                       border-collapse: collapse; /* Bordi uniti */
                       margin: 1em 0; /* Margine sopra/sotto */
                       font-family: "Helvetica Neue", Helvetica, Arial, sans-serif; /* Font simile a Jupyter */
                       font-size: 0.9em; /* Dimensione font leggermente ridotta */
                       border: 1px solid #d3d3d3; /* Bordo esterno leggero */
                       width: auto; /* Larghezza basata sul contenuto */
                       max-width: 100%; /* Non superare il contenitore */
                       overflow-x: auto; /* Abilita lo scroll orizzontale se necessario (meglio sul wrapper, ma ok qui) */
                       display: block; /* Necessario per far funzionare overflow-x su una tabella */
                   }

                   /* Stile per le celle dell'header (th) */
                   .jupyter-style-table thead th {
                       background-color: #f5f5f5; /* Sfondo grigio chiaro per header */
                       font-weight: bold; /* Grassetto */
                       padding: 8px 10px; /* Padding interno */
                       text-align: right; /* Allineamento testo (spesso a destra per numeri/default) */
                       border-bottom: 1px solid #d3d3d3; /* Linea sotto l'header */
                       vertical-align: bottom; /* Allineamento verticale */
                   }

                   /* Stile per le celle dei dati (td) */
                   .jupyter-style-table tbody td {
                       padding: 6px 10px; /* Padding interno */
                       text-align: right; /* Allineamento testo (aggiusta se hai testo a sinistra) */
                       border-right: 1px solid #d3d3d3; /* Linea verticale tra celle (opzionale) */
                       border-top: 1px solid #d3d3d3; /* Linea orizzontale tra righe */
                       vertical-align: middle; /* Allineamento verticale */
                   }
                   .jupyter-style-table tbody td:last-child {
                       border-right: none; /* Rimuovi bordo destro sull'ultima cella */
                   }

                   /* Stile per l'header dell'indice (se presente) */
                   .jupyter-style-table thead th.blank { /* Header vuoto sopra l'indice */
                       background-color: white;
                       border: none;
                   }
                   .jupyter-style-table tbody th { /* Celle dell'indice nel body */
                       padding: 6px 10px;
                       text-align: right;
                       font-weight: normal;
                       border-right: 1px solid #d3d3d3;
                       border-top: 1px solid #d3d3d3;
                       background-color: #f5f5f5; /* Sfondo leggero per indice */
                   }


                   /* Striping delle righe (alternanza colori) */
                   .jupyter-style-table tbody tr:nth-child(even) {
                       background-color: #f9f9f9; /* Sfondo molto leggero per righe pari */
                   }

                   /* Effetto Hover (cambio colore al passaggio del mouse) */
                   .jupyter-style-table tbody tr:hover {
                       background-color: #f0f0f0; /* Sfondo leggermente più scuro su hover */
                   }
                </style>
                <table border="0" class="jupyter-style-table">  <thead>    <tr style="text-align: right;">      <th></th>      <th>feature_B</th>      <th>feature_C</th>      <th>target</th>      <th>feature_A1</th>      <th>feature_A2</th>      <th>sample_col</th>    </tr>  </thead>  <tbody>    <tr>      <th>0</th>      <td>34.835708</td>      <td>Z</td>      <td>75.013312</td>      <td>-0.270712</td>      <td>-0.812137</td>      <td>train</td>    </tr>    <tr>      <th>1</th>      <td>3.086785</td>      <td>X</td>      <td>109.194174</td>      <td>0.104848</td>      <td>0.314544</td>      <td>train</td>    </tr>    <tr>      <th>2</th>      <td>42.384427</td>      <td>Y</td>      <td>96.287048</td>      <td>0.250528</td>      <td>0.751583</td>      <td>train</td>    </tr>    <tr>      <th>3</th>      <td>86.151493</td>      <td>X</td>      <td>264.905765</td>      <td>-0.925200</td>      <td>-2.775600</td>      <td>train</td>    </tr>    <tr>      <th>4</th>      <td>-1.707669</td>      <td>V</td>      <td>2.880829</td>      <td>0.567144</td>      <td>1.701431</td>      <td>train</td>    </tr>    <tr>      <th>5</th>      <td>-1.706848</td>      <td>V</td>      <td>2.318509</td>      <td>-1.040180</td>      <td>-3.120541</td>      <td>train</td>    </tr>    <tr>      <th>6</th>      <td>88.960641</td>      <td>X</td>      <td>273.054387</td>      <td>-0.153676</td>      <td>-0.461028</td>      <td>train</td>    </tr>    <tr>      <th>7</th>      <td>48.371736</td>      <td>V</td>      <td>101.779140</td>      <td>0.789852</td>      <td>2.369555</td>      <td>train</td>    </tr>    <tr>      <th>8</th>      <td>-13.473719</td>      <td>Z</td>      <td>-25.266714</td>      <td>-1.226216</td>      <td>-3.678648</td>      <td>train</td>    </tr>    <tr>      <th>9</th>      <td>37.128002</td>      <td>Y</td>      <td>73.118623</td>      <td>-0.948007</td>      <td>-2.844021</td>      <td>train</td>    </tr>    <tr>      <th>10</th>      <td>-13.170885</td>      <td>X</td>      <td>69.538553</td>      <td>-0.569654</td>      <td>-1.708962</td>      <td>train</td>    </tr>    <tr>      <th>11</th>      <td>-13.286488</td>      <td>Z</td>      <td>-30.168523</td>      <td>-0.977150</td>      <td>-2.931451</td>      <td>train</td>    </tr>    <tr>      <th>12</th>      <td>22.098114</td>      <td>W</td>      <td>54.445288</td>      <td>-0.770632</td>      <td>-2.311895</td>      <td>train</td>    </tr>    <tr>      <th>13</th>      <td>-85.664012</td>      <td>W</td>      <td>-171.324610</td>      <td>-0.033711</td>      <td>-0.101134</td>      <td>train</td>    </tr>    <tr>      <th>14</th>      <td>-76.245892</td>      <td>X</td>      <td>-48.581133</td>      <td>-1.032859</td>      <td>-3.098578</td>      <td>train</td>    </tr>    <tr>      <th>15</th>      <td>-18.114376</td>      <td>X</td>      <td>59.816750</td>      <td>1.142427</td>      <td>3.427282</td>      <td>train</td>    </tr>    <tr>      <th>16</th>      <td>-40.641556</td>      <td>Z</td>      <td>-85.182377</td>      <td>-0.609778</td>      <td>-1.829334</td>      <td>train</td>    </tr>    <tr>      <th>17</th>      <td>25.712367</td>      <td>Y</td>      <td>56.834657</td>      <td>1.469416</td>      <td>4.408249</td>      <td>train</td>    </tr>    <tr>      <th>18</th>      <td>-35.401204</td>      <td>Y</td>      <td>-77.550289</td>      <td>1.492679</td>      <td>4.478037</td>      <td>train</td>    </tr>    <tr>      <th>19</th>      <td>-60.615185</td>      <td>Y</td>      <td>-123.306439</td>      <td>0.707125</td>      <td>2.121376</td>      <td>train</td>    </tr>  </tbody></table>

        **Esempio:**

        >>> from cefeste.selection import FeatureSelection
        >>> fs = FeatureSelection(
        ...  db=df_test_filters,
        ...  target_col='target',
        ...  sample_col='sample_col',
        ...  sample_train_value='train',
        ...  verbose=True
        ... )
        >>> fs.run()
        >>> fs.make_report()

        .. raw:: html

            <table border="0" class="jupyter-style-table">  <thead>    <tr style="text-align: right;">      <th></th>      <th>feat_name</th>      <th>result</th>      <th>drop_reason</th>    </tr>  </thead>  <tbody>    <tr>      <th>0</th>      <td>feature_A1</td>      <td>drop</td>      <td>unexplanatory</td>    </tr>    <tr>      <th>1</th>      <td>feature_A2</td>      <td>drop</td>      <td>unexplanatory</td>    </tr>    <tr>      <th>2</th>      <td>feature_C</td>      <td>keep</td>      <td>NaN</td>    </tr>    <tr>      <th>3</th>      <td>feature_B</td>      <td>keep</td>      <td>NaN</td>    </tr>  </tbody></table>

        >>> fs.get_db_filtered()

        .. raw:: html

            <table border="0" class="jupyter-style-table">  <thead>    <tr style="text-align: right;">      <th></th>      <th>feature_B</th>      <th>feature_C</th>      <th>target</th>      <th>sample_col</th>    </tr>  </thead>  <tbody>    <tr>      <th>0</th>      <td>34.835708</td>      <td>Z</td>      <td>75.013312</td>      <td>train</td>    </tr>    <tr>      <th>1</th>      <td>3.086785</td>      <td>X</td>      <td>109.194174</td>      <td>train</td>    </tr>    <tr>      <th>2</th>      <td>42.384427</td>      <td>Y</td>      <td>96.287048</td>      <td>train</td>    </tr>    <tr>      <th>3</th>      <td>86.151493</td>      <td>X</td>      <td>264.905765</td>      <td>train</td>    </tr>    <tr>      <th>4</th>      <td>-1.707669</td>      <td>V</td>      <td>2.880829</td>      <td>train</td>    </tr>    <tr>      <th>5</th>      <td>-1.706848</td>      <td>V</td>      <td>2.318509</td>      <td>train</td>    </tr>    <tr>      <th>6</th>      <td>88.960641</td>      <td>X</td>      <td>273.054387</td>      <td>train</td>    </tr>    <tr>      <th>7</th>      <td>48.371736</td>      <td>V</td>      <td>101.779140</td>      <td>train</td>    </tr>    <tr>      <th>8</th>      <td>-13.473719</td>      <td>Z</td>      <td>-25.266714</td>      <td>train</td>    </tr>    <tr>      <th>9</th>      <td>37.128002</td>      <td>Y</td>      <td>73.118623</td>      <td>train</td>    </tr>    <tr>      <th>10</th>      <td>-13.170885</td>      <td>X</td>      <td>69.538553</td>      <td>train</td>    </tr>    <tr>      <th>11</th>      <td>-13.286488</td>      <td>Z</td>      <td>-30.168523</td>      <td>train</td>    </tr>    <tr>      <th>12</th>      <td>22.098114</td>      <td>W</td>      <td>54.445288</td>      <td>train</td>    </tr>    <tr>      <th>13</th>      <td>-85.664012</td>      <td>W</td>      <td>-171.324610</td>      <td>train</td>    </tr>    <tr>      <th>14</th>      <td>-76.245892</td>      <td>X</td>      <td>-48.581133</td>      <td>train</td>    </tr>    <tr>      <th>15</th>      <td>-18.114376</td>      <td>X</td>      <td>59.816750</td>      <td>train</td>    </tr>    <tr>      <th>16</th>      <td>-40.641556</td>      <td>Z</td>      <td>-85.182377</td>      <td>train</td>    </tr>    <tr>      <th>17</th>      <td>25.712367</td>      <td>Y</td>      <td>56.834657</td>      <td>train</td>    </tr>    <tr>      <th>18</th>      <td>-35.401204</td>      <td>Y</td>      <td>-77.550289</td>      <td>train</td>    </tr>    <tr>      <th>19</th>      <td>-60.615185</td>      <td>Y</td>      <td>-123.306439</td>      <td>train</td>    </tr>  </tbody></table>
        """
        return self.db.drop(columns=self._filtered_out_features)

    def make_funnel(self):
        """Restituisce un `DataFrame` che riassume il funnel di selezione delle feature.

        Questo `DataFrame` dettaglia ogni passaggio del processo di filtraggio applicato. Per ogni passaggio, mostra il numero di colonne rimosse, il numero di colonne mantenute fino a quel punto e i parametri utilizzati per quel specifico filtro.

        Args:
            `None`: (metodo basato sui risultati dei filtri selezionati)

        Returns:
            `pd.DataFrame`: Un `DataFrame` con le seguenti colonne:

                - **Step_Number** (indice): Numero progressivo del passaggio.
                - **Step_Description**: Descrizione del filtro applicato.
                - **Col_Removed**: Numero di colonne rimosse in quel passaggio.
                - **Col_Kept**: Numero di colonne rimaste dopo quel passaggio.
                - **Params**: Dizionario dei parametri usati per il filtro.

        **Dati utilizzati per gli esempi:**

        >>> df_test_filters

        .. raw:: html

            <style>
                   /* Stile base per la tabella con la nostra classe specifica */
                   .jupyter-style-table {
                       border-collapse: collapse; /* Bordi uniti */
                       margin: 1em 0; /* Margine sopra/sotto */
                       font-family: "Helvetica Neue", Helvetica, Arial, sans-serif; /* Font simile a Jupyter */
                       font-size: 0.9em; /* Dimensione font leggermente ridotta */
                       border: 1px solid #d3d3d3; /* Bordo esterno leggero */
                       width: auto; /* Larghezza basata sul contenuto */
                       max-width: 100%; /* Non superare il contenitore */
                       overflow-x: auto; /* Abilita lo scroll orizzontale se necessario (meglio sul wrapper, ma ok qui) */
                       display: block; /* Necessario per far funzionare overflow-x su una tabella */
                   }

                   /* Stile per le celle dell'header (th) */
                   .jupyter-style-table thead th {
                       background-color: #f5f5f5; /* Sfondo grigio chiaro per header */
                       font-weight: bold; /* Grassetto */
                       padding: 8px 10px; /* Padding interno */
                       text-align: right; /* Allineamento testo (spesso a destra per numeri/default) */
                       border-bottom: 1px solid #d3d3d3; /* Linea sotto l'header */
                       vertical-align: bottom; /* Allineamento verticale */
                   }

                   /* Stile per le celle dei dati (td) */
                   .jupyter-style-table tbody td {
                       padding: 6px 10px; /* Padding interno */
                       text-align: right; /* Allineamento testo (aggiusta se hai testo a sinistra) */
                       border-right: 1px solid #d3d3d3; /* Linea verticale tra celle (opzionale) */
                       border-top: 1px solid #d3d3d3; /* Linea orizzontale tra righe */
                       vertical-align: middle; /* Allineamento verticale */
                   }
                   .jupyter-style-table tbody td:last-child {
                       border-right: none; /* Rimuovi bordo destro sull'ultima cella */
                   }

                   /* Stile per l'header dell'indice (se presente) */
                   .jupyter-style-table thead th.blank { /* Header vuoto sopra l'indice */
                       background-color: white;
                       border: none;
                   }
                   .jupyter-style-table tbody th { /* Celle dell'indice nel body */
                       padding: 6px 10px;
                       text-align: right;
                       font-weight: normal;
                       border-right: 1px solid #d3d3d3;
                       border-top: 1px solid #d3d3d3;
                       background-color: #f5f5f5; /* Sfondo leggero per indice */
                   }


                   /* Striping delle righe (alternanza colori) */
                   .jupyter-style-table tbody tr:nth-child(even) {
                       background-color: #f9f9f9; /* Sfondo molto leggero per righe pari */
                   }

                   /* Effetto Hover (cambio colore al passaggio del mouse) */
                   .jupyter-style-table tbody tr:hover {
                       background-color: #f0f0f0; /* Sfondo leggermente più scuro su hover */
                   }
                </style>
                <table border="0" class="jupyter-style-table">  <thead>    <tr style="text-align: right;">      <th></th>      <th>feature_B</th>      <th>feature_C</th>      <th>target</th>      <th>feature_A1</th>      <th>feature_A2</th>      <th>sample_col</th>    </tr>  </thead>  <tbody>    <tr>      <th>0</th>      <td>34.835708</td>      <td>Z</td>      <td>75.013312</td>      <td>-0.270712</td>      <td>-0.812137</td>      <td>train</td>    </tr>    <tr>      <th>1</th>      <td>3.086785</td>      <td>X</td>      <td>109.194174</td>      <td>0.104848</td>      <td>0.314544</td>      <td>train</td>    </tr>    <tr>      <th>2</th>      <td>42.384427</td>      <td>Y</td>      <td>96.287048</td>      <td>0.250528</td>      <td>0.751583</td>      <td>train</td>    </tr>    <tr>      <th>3</th>      <td>86.151493</td>      <td>X</td>      <td>264.905765</td>      <td>-0.925200</td>      <td>-2.775600</td>      <td>train</td>    </tr>    <tr>      <th>4</th>      <td>-1.707669</td>      <td>V</td>      <td>2.880829</td>      <td>0.567144</td>      <td>1.701431</td>      <td>train</td>    </tr>    <tr>      <th>5</th>      <td>-1.706848</td>      <td>V</td>      <td>2.318509</td>      <td>-1.040180</td>      <td>-3.120541</td>      <td>train</td>    </tr>    <tr>      <th>6</th>      <td>88.960641</td>      <td>X</td>      <td>273.054387</td>      <td>-0.153676</td>      <td>-0.461028</td>      <td>train</td>    </tr>    <tr>      <th>7</th>      <td>48.371736</td>      <td>V</td>      <td>101.779140</td>      <td>0.789852</td>      <td>2.369555</td>      <td>train</td>    </tr>    <tr>      <th>8</th>      <td>-13.473719</td>      <td>Z</td>      <td>-25.266714</td>      <td>-1.226216</td>      <td>-3.678648</td>      <td>train</td>    </tr>    <tr>      <th>9</th>      <td>37.128002</td>      <td>Y</td>      <td>73.118623</td>      <td>-0.948007</td>      <td>-2.844021</td>      <td>train</td>    </tr>    <tr>      <th>10</th>      <td>-13.170885</td>      <td>X</td>      <td>69.538553</td>      <td>-0.569654</td>      <td>-1.708962</td>      <td>train</td>    </tr>    <tr>      <th>11</th>      <td>-13.286488</td>      <td>Z</td>      <td>-30.168523</td>      <td>-0.977150</td>      <td>-2.931451</td>      <td>train</td>    </tr>    <tr>      <th>12</th>      <td>22.098114</td>      <td>W</td>      <td>54.445288</td>      <td>-0.770632</td>      <td>-2.311895</td>      <td>train</td>    </tr>    <tr>      <th>13</th>      <td>-85.664012</td>      <td>W</td>      <td>-171.324610</td>      <td>-0.033711</td>      <td>-0.101134</td>      <td>train</td>    </tr>    <tr>      <th>14</th>      <td>-76.245892</td>      <td>X</td>      <td>-48.581133</td>      <td>-1.032859</td>      <td>-3.098578</td>      <td>train</td>    </tr>    <tr>      <th>15</th>      <td>-18.114376</td>      <td>X</td>      <td>59.816750</td>      <td>1.142427</td>      <td>3.427282</td>      <td>train</td>    </tr>    <tr>      <th>16</th>      <td>-40.641556</td>      <td>Z</td>      <td>-85.182377</td>      <td>-0.609778</td>      <td>-1.829334</td>      <td>train</td>    </tr>    <tr>      <th>17</th>      <td>25.712367</td>      <td>Y</td>      <td>56.834657</td>      <td>1.469416</td>      <td>4.408249</td>      <td>train</td>    </tr>    <tr>      <th>18</th>      <td>-35.401204</td>      <td>Y</td>      <td>-77.550289</td>      <td>1.492679</td>      <td>4.478037</td>      <td>train</td>    </tr>    <tr>      <th>19</th>      <td>-60.615185</td>      <td>Y</td>      <td>-123.306439</td>      <td>0.707125</td>      <td>2.121376</td>      <td>train</td>    </tr>  </tbody></table>

        **Esempio:**

        >>> from cefeste.selection import FeatureSelection
        >>> fs = FeatureSelection(
        ...  db=df_test_filters,
        ...  target_col='target',
        ...  sample_col='sample_col',
        ...  sample_train_value='train',
        ...  verbose=True
        ... )
        >>> fs.run()
        >>> fs.make_report()

        .. raw:: html

            <table border="0" class="jupyter-style-table">  <thead>    <tr style="text-align: right;">      <th></th>      <th>feat_name</th>      <th>result</th>      <th>drop_reason</th>    </tr>  </thead>  <tbody>    <tr>      <th>0</th>      <td>feature_A1</td>      <td>drop</td>      <td>unexplanatory</td>    </tr>    <tr>      <th>1</th>      <td>feature_A2</td>      <td>drop</td>      <td>unexplanatory</td>    </tr>    <tr>      <th>2</th>      <td>feature_C</td>      <td>keep</td>      <td>NaN</td>    </tr>    <tr>      <th>3</th>      <td>feature_B</td>      <td>keep</td>      <td>NaN</td>    </tr>  </tbody></table>

        >>> fs.make_funnel()

        .. raw:: html

            <table border="0" class="jupyter-style-table">  <thead>    <tr style="text-align: right;">      <th></th>      <th>Step_Description</th>      <th>Col_Removed</th>      <th>Col_Kept</th>      <th>Params</th>    </tr>    <tr>      <th>Step_Number</th>      <th></th>      <th></th>      <th></th>      <th></th>    </tr>  </thead>  <tbody>    <tr>      <th>0</th>      <td>Initial feat to check</td>      <td>0</td>      <td>4</td>      <td>NaN</td>    </tr>    <tr>      <th>1</th>      <td>Constant</td>      <td>0</td>      <td>4</td>      <td>NaN</td>    </tr>    <tr>      <th>2</th>      <td>Missing</td>      <td>0</td>      <td>4</td>      <td>{max_pct_missing: 0.9}</td>    </tr>    <tr>      <th>3</th>      <td>Highly Concentrated</td>      <td>0</td>      <td>4</td>      <td>{max_pct_mfv: 0.95}</td>    </tr>    <tr>      <th>4</th>      <td>Unstable</td>      <td>0</td>      <td>4</td>      <td>{max_psi: 0.2, psi_bin_min_pct: 0.02, psi_nbins: 20}</td>    </tr>    <tr>      <th>5</th>      <td>Unexplanatory</td>      <td>2</td>      <td>2</td>      <td>{threshold: 0.05, algo_type: regression, dim_cat_threshold: 10}</td>    </tr>    <tr>      <th>6</th>      <td>Correlated</td>      <td>0</td>      <td>2</td>      <td>{correlation_threshold: 0.95, selection_rule: random, random_state: 42}</td>    </tr></tbody></table>
        """
        return self._funnel_df

    def make_report(self):
        """Genera un report completo che dettaglia lo stato di ogni feature.

        Il report indica se ogni feature inizialmente considerata è stata mantenuta ('keep') o scartata ('drop'). Se una feature è stata scartata, il report specifica anche il motivo della rimozione (cioè, quale filtro l'ha identificata per la rimozione). Se una feature soddisfa i criteri di più filtri, il motivo riportato è generalmente quello del primo filtro (nell'ordine di esecuzione del metodo `run` o nella scelta dell'applicazione dei singoli filtri) che l'ha rimossa.

        Args:
            `None`: (metodo basato sui risultati dei metodi precedenti)

        Returns:
            `pd.DataFrame`: Un `DataFrame` con le seguenti colonne:

                - **feat_name**: Nome della feature.
                - **result**: Stato della feature ('keep' o 'drop').
                - **drop_reason**: Motivo della rimozione (es. 'constant', 'missing'). Se non ci sono motivi di eliminazione verrà riportato `NaN`.

        Note:
            L'ordine dei filtri  determina quale `drop_reason` viene assegnato se una feature è candidata alla rimozione da più filtri.

        **Dati utilizzati per gli esempi:**

        >>> df_test_filters

        .. raw:: html

            <style>
                   /* Stile base per la tabella con la nostra classe specifica */
                   .jupyter-style-table {
                       border-collapse: collapse; /* Bordi uniti */
                       margin: 1em 0; /* Margine sopra/sotto */
                       font-family: "Helvetica Neue", Helvetica, Arial, sans-serif; /* Font simile a Jupyter */
                       font-size: 0.9em; /* Dimensione font leggermente ridotta */
                       border: 1px solid #d3d3d3; /* Bordo esterno leggero */
                       width: auto; /* Larghezza basata sul contenuto */
                       max-width: 100%; /* Non superare il contenitore */
                       overflow-x: auto; /* Abilita lo scroll orizzontale se necessario (meglio sul wrapper, ma ok qui) */
                       display: block; /* Necessario per far funzionare overflow-x su una tabella */
                   }

                   /* Stile per le celle dell'header (th) */
                   .jupyter-style-table thead th {
                       background-color: #f5f5f5; /* Sfondo grigio chiaro per header */
                       font-weight: bold; /* Grassetto */
                       padding: 8px 10px; /* Padding interno */
                       text-align: right; /* Allineamento testo (spesso a destra per numeri/default) */
                       border-bottom: 1px solid #d3d3d3; /* Linea sotto l'header */
                       vertical-align: bottom; /* Allineamento verticale */
                   }

                   /* Stile per le celle dei dati (td) */
                   .jupyter-style-table tbody td {
                       padding: 6px 10px; /* Padding interno */
                       text-align: right; /* Allineamento testo (aggiusta se hai testo a sinistra) */
                       border-right: 1px solid #d3d3d3; /* Linea verticale tra celle (opzionale) */
                       border-top: 1px solid #d3d3d3; /* Linea orizzontale tra righe */
                       vertical-align: middle; /* Allineamento verticale */
                   }
                   .jupyter-style-table tbody td:last-child {
                       border-right: none; /* Rimuovi bordo destro sull'ultima cella */
                   }

                   /* Stile per l'header dell'indice (se presente) */
                   .jupyter-style-table thead th.blank { /* Header vuoto sopra l'indice */
                       background-color: white;
                       border: none;
                   }
                   .jupyter-style-table tbody th { /* Celle dell'indice nel body */
                       padding: 6px 10px;
                       text-align: right;
                       font-weight: normal;
                       border-right: 1px solid #d3d3d3;
                       border-top: 1px solid #d3d3d3;
                       background-color: #f5f5f5; /* Sfondo leggero per indice */
                   }


                   /* Striping delle righe (alternanza colori) */
                   .jupyter-style-table tbody tr:nth-child(even) {
                       background-color: #f9f9f9; /* Sfondo molto leggero per righe pari */
                   }

                   /* Effetto Hover (cambio colore al passaggio del mouse) */
                   .jupyter-style-table tbody tr:hover {
                       background-color: #f0f0f0; /* Sfondo leggermente più scuro su hover */
                   }
                </style>
                <table border="0" class="jupyter-style-table">  <thead>    <tr style="text-align: right;">      <th></th>      <th>feature_B</th>      <th>feature_C</th>      <th>target</th>      <th>feature_A1</th>      <th>feature_A2</th>      <th>sample_col</th>    </tr>  </thead>  <tbody>    <tr>      <th>0</th>      <td>34.835708</td>      <td>Z</td>      <td>75.013312</td>      <td>-0.270712</td>      <td>-0.812137</td>      <td>train</td>    </tr>    <tr>      <th>1</th>      <td>3.086785</td>      <td>X</td>      <td>109.194174</td>      <td>0.104848</td>      <td>0.314544</td>      <td>train</td>    </tr>    <tr>      <th>2</th>      <td>42.384427</td>      <td>Y</td>      <td>96.287048</td>      <td>0.250528</td>      <td>0.751583</td>      <td>train</td>    </tr>    <tr>      <th>3</th>      <td>86.151493</td>      <td>X</td>      <td>264.905765</td>      <td>-0.925200</td>      <td>-2.775600</td>      <td>train</td>    </tr>    <tr>      <th>4</th>      <td>-1.707669</td>      <td>V</td>      <td>2.880829</td>      <td>0.567144</td>      <td>1.701431</td>      <td>train</td>    </tr>    <tr>      <th>5</th>      <td>-1.706848</td>      <td>V</td>      <td>2.318509</td>      <td>-1.040180</td>      <td>-3.120541</td>      <td>train</td>    </tr>    <tr>      <th>6</th>      <td>88.960641</td>      <td>X</td>      <td>273.054387</td>      <td>-0.153676</td>      <td>-0.461028</td>      <td>train</td>    </tr>    <tr>      <th>7</th>      <td>48.371736</td>      <td>V</td>      <td>101.779140</td>      <td>0.789852</td>      <td>2.369555</td>      <td>train</td>    </tr>    <tr>      <th>8</th>      <td>-13.473719</td>      <td>Z</td>      <td>-25.266714</td>      <td>-1.226216</td>      <td>-3.678648</td>      <td>train</td>    </tr>    <tr>      <th>9</th>      <td>37.128002</td>      <td>Y</td>      <td>73.118623</td>      <td>-0.948007</td>      <td>-2.844021</td>      <td>train</td>    </tr>    <tr>      <th>10</th>      <td>-13.170885</td>      <td>X</td>      <td>69.538553</td>      <td>-0.569654</td>      <td>-1.708962</td>      <td>train</td>    </tr>    <tr>      <th>11</th>      <td>-13.286488</td>      <td>Z</td>      <td>-30.168523</td>      <td>-0.977150</td>      <td>-2.931451</td>      <td>train</td>    </tr>    <tr>      <th>12</th>      <td>22.098114</td>      <td>W</td>      <td>54.445288</td>      <td>-0.770632</td>      <td>-2.311895</td>      <td>train</td>    </tr>    <tr>      <th>13</th>      <td>-85.664012</td>      <td>W</td>      <td>-171.324610</td>      <td>-0.033711</td>      <td>-0.101134</td>      <td>train</td>    </tr>    <tr>      <th>14</th>      <td>-76.245892</td>      <td>X</td>      <td>-48.581133</td>      <td>-1.032859</td>      <td>-3.098578</td>      <td>train</td>    </tr>    <tr>      <th>15</th>      <td>-18.114376</td>      <td>X</td>      <td>59.816750</td>      <td>1.142427</td>      <td>3.427282</td>      <td>train</td>    </tr>    <tr>      <th>16</th>      <td>-40.641556</td>      <td>Z</td>      <td>-85.182377</td>      <td>-0.609778</td>      <td>-1.829334</td>      <td>train</td>    </tr>    <tr>      <th>17</th>      <td>25.712367</td>      <td>Y</td>      <td>56.834657</td>      <td>1.469416</td>      <td>4.408249</td>      <td>train</td>    </tr>    <tr>      <th>18</th>      <td>-35.401204</td>      <td>Y</td>      <td>-77.550289</td>      <td>1.492679</td>      <td>4.478037</td>      <td>train</td>    </tr>    <tr>      <th>19</th>      <td>-60.615185</td>      <td>Y</td>      <td>-123.306439</td>      <td>0.707125</td>      <td>2.121376</td>      <td>train</td>    </tr>  </tbody></table>

        **Esempio:**

        >>> from cefeste.selection import FeatureSelection
        >>> fs = FeatureSelection(
        ...  db=df_test_filters,
        ...  target_col='target',
        ...  sample_col='sample_col',
        ...  sample_train_value='train',
        ...  verbose=True
        ... )
        >>> fs.run()
        >>> fs.make_report()

        .. raw:: html

            <table border="0" class="jupyter-style-table">  <thead>    <tr style="text-align: right;">      <th></th>      <th>feat_name</th>      <th>result</th>      <th>drop_reason</th>    </tr>  </thead>  <tbody>    <tr>      <th>0</th>      <td>feature_A1</td>      <td>drop</td>      <td>unexplanatory</td>    </tr>    <tr>      <th>1</th>      <td>feature_A2</td>      <td>drop</td>      <td>unexplanatory</td>    </tr>    <tr>      <th>2</th>      <td>feature_C</td>      <td>keep</td>      <td>NaN</td>    </tr>    <tr>      <th>3</th>      <td>feature_B</td>      <td>keep</td>      <td>NaN</td>    </tr>  </tbody></table>
        """
        attr_list = [
            "_constant_features",
            "_missing_features",
            "_highly_concentrated_features",
            "_low_values_features",
            "_unstable_features",
            "_unexplanatory_features",
            "_correlated_features",
            "_collinear_features",
        ]
        report_list = []

        for attr in attr_list:
            report_list.append(
                pd.DataFrame({"feat_name": self.__dict__[attr], "result": "drop", "drop_reason": attr[1:-9]})
            )
        report_list.append(pd.DataFrame({"feat_name": self._selected_features, "result": "keep"}))

        return pd.concat(report_list).reset_index(drop=True)

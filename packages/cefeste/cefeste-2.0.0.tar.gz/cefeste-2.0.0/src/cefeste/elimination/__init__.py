"""Classe utilizzata per implementare tecniche di eliminazione delle feature."""
from cefeste import FeatureAnalysis
from cefeste.utils import get_categorical_features, convert_Int_series, convert_Int_dataframe
from cefeste.elimination.shap_rfe import Shap_RFE_full
import warnings

from sklearn.model_selection import RandomizedSearchCV, StratifiedKFold


class FeatureElimination(FeatureAnalysis):
    """Classe utilizzata per implementare tecniche di eliminazione delle feature.

    Questa classe orchestra il processo di Recursive Feature Elimination (RFE) utilizzando i valori SHAP come metrica di importanza delle feature. Gestisce la preparazione dei dati, la cross-validation, l'ottimizzazione degli iperparametri (opzionale), l'applicazione di OHE (opzionale) e la selezione finale delle feature basata su diverse regole.

    La classe applica un meccanismo di Feature Selection in-training, ovvero un modello viene addestrato in modo iterativo e ad ogni iterazione viene calcolato l'impatto che le feature hanno sulle predizioni del modello, quindi vengono tolte le feature che hanno un impatto minore finchè non vi è una descrescita critica sulle performance del modello.
    """

    def __init__(
        self,
        # DB / Feature Parameters / Model
        db,
        target_col,
        model,
        grid,
        feat_to_check=None,
        sample_col=None,
        sample_train_value=None,
        algo_type="auto",
        # Hyperparameters Tuning / Cross Validation Fold
        cv_funct=RandomizedSearchCV,
        cv_scoring="auto",
        n_iter=20,
        manage_groups=False,
        groups=None,
        cv_type=StratifiedKFold(5, random_state=42, shuffle=True),
        use_ohe=False,
        # Reporting
        step_size=0.1,
        min_n_feat_step=5,
        final_n_feature=1,
        verbose=True,
        write_final=False,
        write_substep=False,
        dim_cat_threshold=10,
    ):
        """Inizializza l'istanza di FeatureElimination.

        Questo costruttore imposta tutti i parametri necessari per eseguire l'analisi di eliminazione delle feature. Valida gli input, determina automaticamente il tipo di problema di machine learning (se non specificato) e prepara gli attributi della classe.

        Args:
            db (`pd.DataFrame`): `DataFrame` da analizzare.
            target_col (`str`): Nome della colonna target.
            model (`object`): Istanza di un classificatore o regressore.
            grid (`dict`): Griglia degli iperparametri.
            feat_to_check (`list`, optional): Lista delle feature da analizzare. Se `None`, vengono utilizzate tutte le colonne tranne `target_col` e `sample_col`. Default: `None`.
            sample_col (`str`, optional): Nome della colonna che indica se i campioni appartengono a 'train' o 'test'. Default: `None`.
            sample_train_value (`str`, optional): Valore nella `sample_col` che identifica il set di training. Richiesto se `sample_col` è specificato. Default: `None`.
            algo_type (`str`, optional): Tipo di problema: "auto", "classification", "multiclass", "regression". Se "auto", viene dedotto dalla cardinalità della colonna target. Default: "auto".
            cv_funct (`class`, optional): Classe per la ricerca degli iperparametri in cross-validation (es. RandomizedSearchCV, GridSearchCV). Default: `RandomizedSearchCV`.
            cv_scoring (`str`, optional): Metrica di scoring da usare nella cross-validation. Se "auto", seleziona "roc_auc" per classificazione binaria, "r2" per regressione e "balanced_accuracy" per multiclasse. Default: "auto".
            n_iter (int, optional): Numero di iterazioni (combinazioni di iperparametri) da testare nella ricerca degli iperparametri. Default: `20`.
            manage_groups (`bool`, optional): Se `True`, indica che la cross-validation deve mantenere uniti i gruppi definiti nel parametro `groups`. Default: `False`.
            groups (`pd.Series`, optional): `Series` con indice allineato al parametro `db`, contenente gli identificatori dei gruppi per la cross-validation (usato se `manage_groups` è `True`). Default: `None`.
            cv_type (`class`, optional): Classe splitter per definire i fold della cross-validation (es. StratifiedKFold, GroupKFold). Default: `StratifiedKFold(5, random_state=42, shuffle=True)`.
            use_ohe (`bool`, optional): Se `True`, applica One-Hot Encoding alle feature identificate come categoriche prima di passare i dati al modello. Default: `False`.
            step_size (`int`/`float`, optional): Numero o frazione di feature da rimuovere ad ogni passo dell'RFE. Default: 0.1 (10%).
            min_n_feat_step (`int`, optional): Numero minimo di feature da rimuovere ad ogni passo, anche se `step_size` (come frazione) risulta in un numero minore. Default: 5.
            final_n_feature (`int`, optional): Numero minimo di feature a cui fermare il processo RFE. Default: 1.
            verbose (`bool`, optional): Se `True`, stampa informazioni sull'avanzamento del processo. Default a `True`.
            write_final (`bool`, optional): Se `True`, salva il report finale (`DataFrame`) in un file CSV nella directory corrente. Default: `False`.
            write_substep (`bool`, optional): Se `True`, salva un report intermedio dopo ogni passo di eliminazione SHAP RFE in file CSV. Default: `False`.
            dim_cat_threshold (`int`, optional):  Soglia di cardinalità per le feature categoriche. Se una feature categorica ha più valori unici di questa soglia, solo le top `dim_cat_threshold` categorie più frequenti vengono codificate con One-Hot Encoding (le altre vengono ignorate). Se `None`, viene applicato One-Hot Encoding standard a tutte le categorie. Default: 10.

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
            self._n_sample = None
        # Sample Train value
        if (sample_train_value is not None) & (sample_train_value not in self._sample_list):
            raise ValueError(
                f"The value {sample_train_value} set for parameter sample_train_value is not in {sample_col}."
            )
        else:
            self.sample_train_value = sample_train_value

        # Parameters
        self.model = model
        self.grid = grid
        self.cv_funct = cv_funct
        self.cv_scoring = cv_scoring
        self.n_iter = n_iter
        self.manage_groups = manage_groups
        self.groups = groups
        self.cv_type = cv_type
        self.use_ohe = use_ohe
        self.step_size = step_size
        self.min_n_feat_step = min_n_feat_step
        self.final_n_feature = final_n_feature
        self.verbose = verbose
        self.write_final = write_final
        self.write_substep = write_substep
        self.dim_cat_threshold = dim_cat_threshold
        self.report = None
        self.final_feat = []
        self.selection_rule = None
        self.number_feat_rep = None
        self._filtered_out_features = []

    def make_report(self, **kwargs):
        """Esegue il processo SHAP RFE e genera il report delle performance per ogni iterazione.

        Questo metodo prepara i dati, valida i gruppi per la CV (se presenti), identifica le feature categoriche per OHE (se richiesto), e infine esegue l'eliminazione ricorsiva delle feature. Il report risultante viene memorizzato nell'attributo `report`.


        La **RFE** seleziona le feature per un modello con il seguente processo iterativo:

        - Addestra un modello ottimizzandone gli iperparametri tramite Cross-Validation.
        - Calcola l'importanza di ogni feature usando i valori SHAP.
        - Rimuove le feature meno importanti.
        - Ripete i passaggi finché non rimane il numero desiderato di feature (o finchè non vi è una decrescita critica nelle performance).

        Args:
            **kwargs: Permette di sovrascrivere temporaneamente i parametri impostati durante l'inizializzazione (es. `step_size`, `n_iter`) solo per questa esecuzione.

        Returns:
            `pd.DataFrame`: Un `DataFrame` contenente il report del processo SHAP RFE. Contiene le seguenti colonne:

                - **n_feat**: Numero di feature nel dataset prima della rimozione delle feature in uno step.
                - **train_score**: Metrica di performance (AUC, R2, Balanced Accuracy) del modello addestrato sul dataset di training con le feature correnti.
                - **valid_score**: Metrica di performance di validazione del modello in Cross-Validation sul dataset di training con le feature correnti.
                - **n_feat_to_remove**: Numero di feature rimosse in uno step.
                - **feat_used**: Lista delle feature utilizzate per addestrare il modello in uno step (prima della rimozione).
                - **feat_to_remove**: Lista delle feature che sono state rimosse in questo step.
                - **feat_select**: Lista delle feature selezionate che rimangono nel dataset dopo la rimozione delle feature in uno step. Queste sono le feature che verranno utilizzate nello step successivo (se presente).
                - **best_estimator**: L'oggetto modello (classificatore o regressore) che ha ottenuto le migliori performance durante la Cross-Validation in uno step. Contiene il modello addestrato e i suoi iperparametri ottimizzati.

        **Esempio:**

        >>> import pandas as pd
        >>> from sklearn.linear_model import LogisticRegression
        >>> from cefeste.elimination import FeatureElimination
        >>> # Dati di esempio
        >>> data = pd.DataFrame({
        ... 'feature1': [1,2,3,4,5,6,7,8,9,2,3,1,3,6,43,2,4,6,3,2,6,3,2,6,3,2,5],
        ... 'feature2': [5,4,3,2,1,6,3,7,3,5,8,4,2,9,75,4,5,7,5,2,5,8,6,3,5,7,8],
        ... 'feature3': [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        ... 'feature4': [8,8,8,9,5,3,4,5,6,2,6,8,4,4,4,6,5,7,8,5,9,3,4,7,5,78,8],
        ... 'feature5': [2,12,4,14,2,3,1,2,3,14,1,1,14,12,15,16,2,12,13,12,1,15,17,2,1,15,1],
        ... 'target':   [0,1,0,1,0,0,0,0,0,1,1,1,1,1,1,1,0,1,1,1,0,1,1,0,1,1,1]
        ... })
        >>> # Parametri
        >>> target_col = 'target'
        >>> model = LogisticRegression()
        >>> grid = {'C': [0.1, 1, 10]}
        >>> # Inizializzazione
        >>> fe = FeatureElimination(
        ...    db=data,
        ...    target_col=target_col,
        ...    model=model,
        ...    grid=grid,
        ...    min_n_feat_step=1
        ... )
        >>> # Generazione del report
        >>> fe.make_report()

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
            <table border="0" class="jupyter-style-table">  <thead>    <tr style="text-align: right;">      <th></th>      <th>n_feat</th>      <th>train_score</th>      <th>valid_score</th>      <th>n_feat_to_remove</th>      <th>feat_used</th>      <th>feat_to_remove</th>      <th>feat_select</th>      <th>best_estimator</th>    </tr>  </thead>  <tbody>    <tr>      <th>0</th>      <td>5</td>      <td>0.964706</td>      <td>0.891667</td>      <td>1</td>      <td>[feature3, feature5, feature1, feature2, feature4]</td>      <td>[feature3]</td>      <td>[feature5, feature1, feature2, feature4]</td>      <td>LogisticRegression(C=0.1)</td>    </tr>    <tr>      <th>1</th>      <td>4</td>      <td>0.964706</td>      <td>0.891667</td>      <td>1</td>      <td>[feature4, feature5, feature2, feature1]</td>      <td>[feature4]</td>      <td>[feature5, feature2, feature1]</td>      <td>LogisticRegression(C=0.1)</td>    </tr>    <tr>      <th>2</th>      <td>3</td>      <td>0.982353</td>      <td>0.925000</td>      <td>1</td>      <td>[feature2, feature5, feature1]</td>      <td>[feature2]</td>      <td>[feature5, feature1]</td>      <td>LogisticRegression(C=1)</td>    </tr>    <tr>      <th>3</th>      <td>2</td>      <td>0.817647</td>      <td>0.750000</td>      <td>1</td>      <td>[feature1, feature5]</td>      <td>[feature1]</td>      <td>[feature5]</td>      <td>LogisticRegression(C=0.1)</td>    </tr>    <tr>      <th>4</th>      <td>1</td>      <td>0.788235</td>      <td>0.791667</td>      <td>0</td>      <td>[feature5]</td>      <td>[]</td>      <td>[feature5]</td>      <td>LogisticRegression(C=0.1)</td>    </tr>  </tbody></table>
        """
        self.set_params(**kwargs)
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
            raise ValueError("shap rfe not performed since no target column defined")
        X = X[self.feat_to_check]

        if self.sample_train_value is not None:
            X_train = X.loc[sample_series == self.sample_train_value]
            y_train = y.loc[sample_series == self.sample_train_value]
        else:
            X_train = X
            y_train = y

        # Groups check
        if self.manage_groups:
            if self.groups is None:
                warnings.warn("no group defined")
                self.manage_groups = False
            elif not self.groups.index.equals(self.db.index):
                raise ValueError("Groups Series index do not match with DataFrame index in input!")
            else:
                self.groups = self.groups.reset_index(drop=True).iloc[X_train.index]
        else:
            self.groups = None

        # Categorical Features for One Hot Encoding
        if self.use_ohe:
            self.categorical_features_list_ohe = get_categorical_features(X_train)
        else:
            self.categorical_features_list_ohe = []

        shap_report = Shap_RFE_full(
            convert_Int_dataframe(X_train),
            convert_Int_series(y_train),
            model=self.model,
            grid=self.grid,
            cv_funct=self.cv_funct,
            cv_scoring=self.cv_scoring,
            n_iter=self.n_iter,
            manage_groups=self.manage_groups,
            groups=self.groups,
            cv_type=self.cv_type,
            algo_type=self.algo_type,
            step_size=self.step_size,
            min_n_feat_step=self.min_n_feat_step,
            final_n_feature=self.final_n_feature,
            verbose=self.verbose,
            write_final=self.write_final,
            write_substep=self.write_substep,
            use_ohe=self.use_ohe,
            categorical_features_list_ohe=self.categorical_features_list_ohe,
            dim_cat_threshold=self.dim_cat_threshold,
        )

        self.report = shap_report

        return self.report

    def plot_report(self):
        """Genera un grafico delle performance (train e validation score) rispetto al numero di feature.

        Utilizza il `DataFrame` dell'attributo `report` generato dal metodo `make_report()` per creare un grafico a linee che mostra l'andamento dello score di training e di validazione man mano che le feature vengono eliminate. L'asse x rappresenta il numero di feature, l'asse y lo score.

        Args:
            `None`: (metodo basato sul report risultante dal metodo `make_report()`).

        **Esempio:**

        >>> import pandas as pd
        >>> from sklearn.linear_model import LogisticRegression
        >>> from cefeste.elimination import FeatureElimination
        >>> # Dati di esempio
        >>> data = pd.DataFrame({
        ... 'feature1': [1,2,3,4,5,6,7,8,9,2,3,1,3,6,43,2,4,6,3,2,6,3,2,6,3,2,5],
        ... 'feature2': [5,4,3,2,1,6,3,7,3,5,8,4,2,9,75,4,5,7,5,2,5,8,6,3,5,7,8],
        ... 'feature3': [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        ... 'feature4': [8,8,8,9,5,3,4,5,6,2,6,8,4,4,4,6,5,7,8,5,9,3,4,7,5,78,8],
        ... 'feature5': [2,12,4,14,2,3,1,2,3,14,1,1,14,12,15,16,2,12,13,12,1,15,17,2,1,15,1],
        ... 'target':   [0,1,0,1,0,0,0,0,0,1,1,1,1,1,1,1,0,1,1,1,0,1,1,0,1,1,1]
        ... })
        >>> # Parametri
        >>> target_col = 'target'
        >>> model = LogisticRegression()
        >>> grid = {'C': [0.1, 1, 10]}
        >>> # Inizializzazione
        >>> fe = FeatureElimination(
        ...    db=data,
        ...    target_col=target_col,
        ...    model=model,
        ...    grid=grid,
        ...    min_n_feat_step=1
        ... )
        >>> # Generazione del report
        >>> fe.make_report()

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
            <table border="0" class="jupyter-style-table">  <thead>    <tr style="text-align: right;">      <th></th>      <th>n_feat</th>      <th>train_score</th>      <th>valid_score</th>      <th>n_feat_to_remove</th>      <th>feat_used</th>      <th>feat_to_remove</th>      <th>feat_select</th>      <th>best_estimator</th>    </tr>  </thead>  <tbody>    <tr>      <th>0</th>      <td>5</td>      <td>0.964706</td>      <td>0.891667</td>      <td>1</td>      <td>[feature3, feature5, feature1, feature2, feature4]</td>      <td>[feature3]</td>      <td>[feature5, feature1, feature2, feature4]</td>      <td>LogisticRegression(C=0.1)</td>    </tr>    <tr>      <th>1</th>      <td>4</td>      <td>0.964706</td>      <td>0.891667</td>      <td>1</td>      <td>[feature4, feature5, feature2, feature1]</td>      <td>[feature4]</td>      <td>[feature5, feature2, feature1]</td>      <td>LogisticRegression(C=0.1)</td>    </tr>    <tr>      <th>2</th>      <td>3</td>      <td>0.982353</td>      <td>0.925000</td>      <td>1</td>      <td>[feature2, feature5, feature1]</td>      <td>[feature2]</td>      <td>[feature5, feature1]</td>      <td>LogisticRegression(C=1)</td>    </tr>    <tr>      <th>3</th>      <td>2</td>      <td>0.817647</td>      <td>0.750000</td>      <td>1</td>      <td>[feature1, feature5]</td>      <td>[feature1]</td>      <td>[feature5]</td>      <td>LogisticRegression(C=0.1)</td>    </tr>    <tr>      <th>4</th>      <td>1</td>      <td>0.788235</td>      <td>0.791667</td>      <td>0</td>      <td>[feature5]</td>      <td>[]</td>      <td>[feature5]</td>      <td>LogisticRegression(C=0.1)</td>    </tr>  </tbody></table>

        >>> fe.plot_report()

        .. image:: ../../../build/images/plot_elimination.png

        """
        if self.report is not None:
            self.report.plot(
                x="n_feat", y=["train_score", "valid_score"], xlim=(max(self.report.n_feat), min(self.report.n_feat))
            )
        else:
            raise ValueError("Missing report, run .make_report() first")

    def extract_features(self, selection_rule="decrease_perf", number_feat_rep=None, gap=0.1, alpha=0.5):
        """Estrae la lista finale delle feature selezionate in base a una regola specificata.

        Analizza il report generato dal metodo `make_report()` e seleziona un sottoinsieme di feature secondo il parametro `selection_rule`. Le regole disponibili sono:

        - `decrease_perf`: Seleziona il set di feature più piccolo prima che la performance di validazione scenda significativamente (più del `gap` %) rispetto al massimo raggiunto.
        - `best_valid`: Seleziona il set di feature corrispondente al miglior punteggio di validazione (scegliendo il set più piccolo in caso di parità).
        - `num_feat`: Seleziona il set di feature corrispondente esattamente a `number_feat_rep` feature.
        - `robust_tradeoff`: Seleziona il set di feature che massimizza un compromesso tra performance media (train+valid) e robustezza (gap tra performance di train e valid), pesato dal parametro `alpha`. Viene calcolato come lo score medio (tra train e valid) moltiplicato per `alpha` meno la differenza di score in valore assoluto (tra train e valid) moltiplicato per 1 - `alpha`.

        La lista delle feature selezionate viene memorizzata nell'attributo `final_feat` e restituita dal metodo. Le feature scartate, invece, vengono memorizzate nell'attributo `_filtered_out_features`.

        Args:
            selection_rule (`str`, optional): La regola da utilizzare per la selezione. Valori possibili: "decrease_perf", "best_valid", "num_feat", "robust_tradeoff". Default: 'decrease_perf'.
            number_feat_rep (`int`, optional): Numero di feature desiderato. Utilizzato solo se `selection_rule` è "num_feat". Default: `None`.
            gap (`float`, optional): Soglia di calo percentuale della performance accettabile. Utilizzato solo se `selection_rule` è "decrease_perf". Default: 0.1 (10%).
            alpha (`float`, optional): Peso per il termine di performance medio nella regola "robust_tradeoff". Il peso per il gap di robustezza sarà (1-alpha). Deve essere tra 0 e 1. Default: 0.5.

        Returns:
            `list`: La lista dei nomi delle feature selezionate.

        **Esempio:**

        >>> import pandas as pd
        >>> from sklearn.linear_model import LogisticRegression
        >>> from cefeste.elimination import FeatureElimination
        >>> # Dati di esempio
        >>> data = pd.DataFrame({
        ... 'feature1': [1,2,3,4,5,6,7,8,9,2,3,1,3,6,43,2,4,6,3,2,6,3,2,6,3,2,5],
        ... 'feature2': [5,4,3,2,1,6,3,7,3,5,8,4,2,9,75,4,5,7,5,2,5,8,6,3,5,7,8],
        ... 'feature3': [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        ... 'feature4': [8,8,8,9,5,3,4,5,6,2,6,8,4,4,4,6,5,7,8,5,9,3,4,7,5,78,8],
        ... 'feature5': [2,12,4,14,2,3,1,2,3,14,1,1,14,12,15,16,2,12,13,12,1,15,17,2,1,15,1],
        ... 'target':   [0,1,0,1,0,0,0,0,0,1,1,1,1,1,1,1,0,1,1,1,0,1,1,0,1,1,1]
        ... })
        >>> # Parametri
        >>> target_col = 'target'
        >>> model = LogisticRegression()
        >>> grid = {'C': [0.1, 1, 10]}
        >>> # Inizializzazione
        >>> fe = FeatureElimination(
        ...    db=data,
        ...    target_col=target_col,
        ...    model=model,
        ...    grid=grid,
        ...    min_n_feat_step=1
        ... )
        >>> # Generazione del report
        >>> fe.make_report()

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
            <table border="0" class="jupyter-style-table">  <thead>    <tr style="text-align: right;">      <th></th>      <th>n_feat</th>      <th>train_score</th>      <th>valid_score</th>      <th>n_feat_to_remove</th>      <th>feat_used</th>      <th>feat_to_remove</th>      <th>feat_select</th>      <th>best_estimator</th>    </tr>  </thead>  <tbody>    <tr>      <th>0</th>      <td>5</td>      <td>0.964706</td>      <td>0.891667</td>      <td>1</td>      <td>[feature3, feature5, feature1, feature2, feature4]</td>      <td>[feature3]</td>      <td>[feature5, feature1, feature2, feature4]</td>      <td>LogisticRegression(C=0.1)</td>    </tr>    <tr>      <th>1</th>      <td>4</td>      <td>0.964706</td>      <td>0.891667</td>      <td>1</td>      <td>[feature4, feature5, feature2, feature1]</td>      <td>[feature4]</td>      <td>[feature5, feature2, feature1]</td>      <td>LogisticRegression(C=0.1)</td>    </tr>    <tr>      <th>2</th>      <td>3</td>      <td>0.982353</td>      <td>0.925000</td>      <td>1</td>      <td>[feature2, feature5, feature1]</td>      <td>[feature2]</td>      <td>[feature5, feature1]</td>      <td>LogisticRegression(C=1)</td>    </tr>    <tr>      <th>3</th>      <td>2</td>      <td>0.817647</td>      <td>0.750000</td>      <td>1</td>      <td>[feature1, feature5]</td>      <td>[feature1]</td>      <td>[feature5]</td>      <td>LogisticRegression(C=0.1)</td>    </tr>    <tr>      <th>4</th>      <td>1</td>      <td>0.788235</td>      <td>0.791667</td>      <td>0</td>      <td>[feature5]</td>      <td>[]</td>      <td>[feature5]</td>      <td>LogisticRegression(C=0.1)</td>    </tr>  </tbody></table>

        >>> fe.extract_features()
        ['feature2', 'feature5', 'feature1']

        """
        self.selection_rule = selection_rule
        self.number_feat_rep = number_feat_rep
        self.gap = gap
        self.alpha = alpha
        # Check the target var and set the algo type
        if selection_rule not in ["decrease_perf", "best_valid", "num_feat", "robust_tradeoff"]:
            raise ValueError(
                f"{selection_rule} is not a valid selection_rule. It should be one of the following:\n ['decrease_perf', 'best_valid', 'num_feat', 'robust_tradeoff']"
            )

        if self.report is not None:
            if selection_rule == "decrease_perf":
                # Define n_feat: the first time the validation score decreases of more than 10%
                cutoff = (
                    self.report[["n_feat", "valid_score"]]
                    .sort_values("n_feat", ascending=False)
                    .assign(max_until=lambda x: x.valid_score.expanding().max())
                    .assign(valid_next=lambda x: x.valid_score.shift(periods=-1))
                    .assign(
                        gap=lambda x: x.apply(
                            lambda y: (y.max_until / y.valid_next) - 1
                            if y.valid_next > 0
                            else 1 - (y.max_until / y.valid_next),
                            axis=1,
                        )
                    )
                    .loc[lambda x: x.gap > gap]
                )
                if cutoff.shape[0] < 1:
                    cutoff = self.report.loc[self.report.n_feat.idxmin(), "n_feat"]
                else:
                    cutoff = cutoff.loc[lambda x: x.n_feat.idxmax(), "n_feat"]

                self.final_feat = list(self.report.loc[self.report["n_feat"] == cutoff, "feat_used"])[0]

            elif selection_rule == "best_valid":
                # Define n_feat: best validation score iteration
                n_min_feat = self.report.loc[
                    self.report["valid_score"] == self.report["valid_score"].max(), "n_feat"
                ].min()
                self.final_feat = list(self.report.loc[self.report["n_feat"] == n_min_feat, "feat_used"])[0]

            elif selection_rule == "robust_tradeoff":
                # Define n_feat: best score of the formula α * Average_Perf - (1-α) * Gap_Robust
                adding_report = (
                    self.report[["n_feat", "train_score", "valid_score"]]
                    .assign(avg_scoring=lambda x: (x.train_score + x.valid_score) / 2)
                    .assign(gap_ratio=lambda x: abs(x.train_score - x.valid_score))
                    .assign(avg_scoring=lambda x: (x.avg_scoring - x.avg_scoring.mean()) / x.avg_scoring.std())
                    .assign(gap_ratio=lambda x: (x.gap_ratio - x.gap_ratio.mean()) / x.gap_ratio.std())
                    .assign(tradeoff_robust_avg_scoring=lambda x: (alpha * x.avg_scoring - (1 - alpha) * x.gap_ratio))
                )
                n_min_feat = adding_report.loc[
                    lambda x: x.tradeoff_robust_avg_scoring == x.tradeoff_robust_avg_scoring.max(),
                    "n_feat",
                ].min()
                self.final_feat = list(self.report.loc[self.report["n_feat"] == n_min_feat, "feat_used"])[0]

            else:
                # Define n_feat: the user choose the features to use according to number of features to be used
                if number_feat_rep is not None:
                    try:
                        self.final_feat = list(self.report.loc[self.report["n_feat"] == number_feat_rep, "feat_used"])[
                            0
                        ]
                    except Exception:
                        raise ValueError(f"{number_feat_rep} number of features chosen uncorrect, look the report")
                else:
                    self.final_feat = list(
                        self.report.loc[self.report["n_feat"] == self.report["n_feat"].max(), "feat_used"]
                    )[0]
        else:
            raise ValueError("Missing report, run .make_report() first")

        self._filtered_out_features = list(set(self.feat_to_check) - set(self.final_feat))
        return self.final_feat

    def get_X_original(self):
        """Restituisce il `DataFrame` originale contenente solo le feature inizialmente considerate.

        Seleziona dal `DataFrame` originale (attributo `db`) solo le colonne presenti nell'attributo `feat_to_check`, ovvero le feature che sono state incluse all'inizio del processo di analisi/eliminazione.

        Returns:
            `pd.DataFrame`: Un `DataFrame` contenente solo le colonne specificate in `feat_to_check`.

        **Esempio:**

        >>> import pandas as pd
        >>> from sklearn.linear_model import LogisticRegression
        >>> from cefeste.elimination import FeatureElimination
        >>> # Dati di esempio
        >>> data = pd.DataFrame({
        ... 'feature1': [1,2,3,4,5,6,7,8,9,2,3,1,3,6,43,2,4,6,3,2,6,3,2,6,3,2,5],
        ... 'feature2': [5,4,3,2,1,6,3,7,3,5,8,4,2,9,75,4,5,7,5,2,5,8,6,3,5,7,8],
        ... 'feature3': [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        ... 'feature4': [8,8,8,9,5,3,4,5,6,2,6,8,4,4,4,6,5,7,8,5,9,3,4,7,5,78,8],
        ... 'feature5': [2,12,4,14,2,3,1,2,3,14,1,1,14,12,15,16,2,12,13,12,1,15,17,2,1,15,1],
        ... 'target':   [0,1,0,1,0,0,0,0,0,1,1,1,1,1,1,1,0,1,1,1,0,1,1,0,1,1,1]
        ... })
        >>> # Parametri
        >>> target_col = 'target'
        >>> model = LogisticRegression()
        >>> grid = {'C': [0.1, 1, 10]}
        >>> # Inizializzazione
        >>> fe = FeatureElimination(
        ...    db=data,
        ...    target_col=target_col,
        ...    model=model,
        ...    grid=grid,
        ...    min_n_feat_step=1
        ... )
        >>> # Generazione del report
        >>> fe.make_report()

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
            <table border="0" class="jupyter-style-table">  <thead>    <tr style="text-align: right;">      <th></th>      <th>n_feat</th>      <th>train_score</th>      <th>valid_score</th>      <th>n_feat_to_remove</th>      <th>feat_used</th>      <th>feat_to_remove</th>      <th>feat_select</th>      <th>best_estimator</th>    </tr>  </thead>  <tbody>    <tr>      <th>0</th>      <td>5</td>      <td>0.964706</td>      <td>0.891667</td>      <td>1</td>      <td>[feature3, feature5, feature1, feature2, feature4]</td>      <td>[feature3]</td>      <td>[feature5, feature1, feature2, feature4]</td>      <td>LogisticRegression(C=0.1)</td>    </tr>    <tr>      <th>1</th>      <td>4</td>      <td>0.964706</td>      <td>0.891667</td>      <td>1</td>      <td>[feature4, feature5, feature2, feature1]</td>      <td>[feature4]</td>      <td>[feature5, feature2, feature1]</td>      <td>LogisticRegression(C=0.1)</td>    </tr>    <tr>      <th>2</th>      <td>3</td>      <td>0.982353</td>      <td>0.925000</td>      <td>1</td>      <td>[feature2, feature5, feature1]</td>      <td>[feature2]</td>      <td>[feature5, feature1]</td>      <td>LogisticRegression(C=1)</td>    </tr>    <tr>      <th>3</th>      <td>2</td>      <td>0.817647</td>      <td>0.750000</td>      <td>1</td>      <td>[feature1, feature5]</td>      <td>[feature1]</td>      <td>[feature5]</td>      <td>LogisticRegression(C=0.1)</td>    </tr>    <tr>      <th>4</th>      <td>1</td>      <td>0.788235</td>      <td>0.791667</td>      <td>0</td>      <td>[feature5]</td>      <td>[]</td>      <td>[feature5]</td>      <td>LogisticRegression(C=0.1)</td>    </tr>  </tbody></table>

        >>> fe.extract_features()
        ['feature2', 'feature5', 'feature1']

        >>> fe.get_X_original()

        .. raw:: html

            <table border="0" class="jupyter-style-table">  <thead>    <tr style="text-align: right;">      <th></th>      <th>feature4</th>      <th>feature1</th>      <th>feature2</th>      <th>feature3</th>      <th>feature5</th>    </tr>  </thead>  <tbody>    <tr>      <th>0</th>      <td>8</td>      <td>1</td>      <td>5</td>      <td>0</td>      <td>2</td>    </tr>    <tr>      <th>1</th>      <td>8</td>      <td>2</td>      <td>4</td>      <td>0</td>      <td>12</td>    </tr>    <tr>      <th>2</th>      <td>8</td>      <td>3</td>      <td>3</td>      <td>0</td>      <td>4</td>    </tr>    <tr>      <th>3</th>      <td>9</td>      <td>4</td>      <td>2</td>      <td>0</td>      <td>14</td>    </tr>    <tr>      <th>4</th>      <td>5</td>      <td>5</td>      <td>1</td>      <td>0</td>      <td>2</td>    </tr>    <tr>      <th>5</th>      <td>3</td>      <td>6</td>      <td>6</td>      <td>0</td>      <td>3</td>    </tr>    <tr>      <th>6</th>      <td>4</td>      <td>7</td>      <td>3</td>      <td>0</td>      <td>1</td>    </tr>    <tr>      <th>7</th>      <td>5</td>      <td>8</td>      <td>7</td>      <td>0</td>      <td>2</td>    </tr>    <tr>      <th>8</th>      <td>6</td>      <td>9</td>      <td>3</td>      <td>0</td>      <td>3</td>    </tr>    <tr>      <th>9</th>      <td>2</td>      <td>2</td>      <td>5</td>      <td>0</td>      <td>14</td>    </tr>    <tr>      <th>10</th>      <td>6</td>      <td>3</td>      <td>8</td>      <td>0</td>      <td>1</td>    </tr>    <tr>      <th>11</th>      <td>8</td>      <td>1</td>      <td>4</td>      <td>0</td>      <td>1</td>    </tr>    <tr>      <th>12</th>      <td>4</td>      <td>3</td>      <td>2</td>      <td>0</td>      <td>14</td>    </tr>    <tr>      <th>13</th>      <td>4</td>      <td>6</td>      <td>9</td>      <td>0</td>      <td>12</td>    </tr>    <tr>      <th>14</th>      <td>4</td>      <td>43</td>      <td>75</td>      <td>0</td>      <td>15</td>    </tr>    <tr>      <th>15</th>      <td>6</td>      <td>2</td>      <td>4</td>      <td>0</td>      <td>16</td>    </tr>    <tr>      <th>16</th>      <td>5</td>      <td>4</td>      <td>5</td>      <td>0</td>      <td>2</td>    </tr>    <tr>      <th>17</th>      <td>7</td>      <td>6</td>      <td>7</td>      <td>0</td>      <td>12</td>    </tr>    <tr>      <th>18</th>      <td>8</td>      <td>3</td>      <td>5</td>      <td>0</td>      <td>13</td>    </tr>    <tr>      <th>19</th>      <td>5</td>      <td>2</td>      <td>2</td>      <td>0</td>      <td>12</td>    </tr>    <tr>      <th>20</th>      <td>9</td>      <td>6</td>      <td>5</td>      <td>0</td>      <td>1</td>    </tr>    <tr>      <th>21</th>      <td>3</td>      <td>3</td>      <td>8</td>      <td>0</td>      <td>15</td>    </tr>    <tr>      <th>22</th>      <td>4</td>      <td>2</td>      <td>6</td>      <td>0</td>      <td>17</td>    </tr>    <tr>      <th>23</th>      <td>7</td>      <td>6</td>      <td>3</td>      <td>0</td>      <td>2</td>    </tr>    <tr>      <th>24</th>      <td>5</td>      <td>3</td>      <td>5</td>      <td>0</td>      <td>1</td>    </tr>    <tr>      <th>25</th>      <td>78</td>      <td>2</td>      <td>7</td>      <td>0</td>      <td>15</td>    </tr>    <tr>      <th>26</th>      <td>8</td>      <td>5</td>      <td>8</td>      <td>0</td>      <td>1</td>    </tr>  </tbody></table>
        """
        return self.db[self.feat_to_check]

    def get_X_reduced(self):
        """Restituisce il `DataFrame` contenente solo le feature finali selezionate.

        Seleziona dal `DataFrame` originale (attributo `db`) solo le colonne presenti nell'attributo `final_feat`, che è stata popolata dal metodo `extract_features()`. Questo rappresenta il dataset dopo l'applicazione della feature elimination (escluse le colonne `target` e `sample_col`).

        Returns:
            `pd.DataFrame`: Un `DataFrame` contenente solo le colonne delle feature finali selezionate.

        Note:
            Assicurarsi di aver eseguito `make_report()` e `extract_features()` prima di chiamare questo metodo per ottenere un risultato significativo.

        **Esempio:**

        >>> import pandas as pd
        >>> from sklearn.linear_model import LogisticRegression
        >>> from cefeste.elimination import FeatureElimination
        >>> # Dati di esempio
        >>> data = pd.DataFrame({
        ... 'feature1': [1,2,3,4,5,6,7,8,9,2,3,1,3,6,43,2,4,6,3,2,6,3,2,6,3,2,5],
        ... 'feature2': [5,4,3,2,1,6,3,7,3,5,8,4,2,9,75,4,5,7,5,2,5,8,6,3,5,7,8],
        ... 'feature3': [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        ... 'feature4': [8,8,8,9,5,3,4,5,6,2,6,8,4,4,4,6,5,7,8,5,9,3,4,7,5,78,8],
        ... 'feature5': [2,12,4,14,2,3,1,2,3,14,1,1,14,12,15,16,2,12,13,12,1,15,17,2,1,15,1],
        ... 'target':   [0,1,0,1,0,0,0,0,0,1,1,1,1,1,1,1,0,1,1,1,0,1,1,0,1,1,1]
        ... })
        >>> # Parametri
        >>> target_col = 'target'
        >>> model = LogisticRegression()
        >>> grid = {'C': [0.1, 1, 10]}
        >>> # Inizializzazione
        >>> fe = FeatureElimination(
        ...    db=data,
        ...    target_col=target_col,
        ...    model=model,
        ...    grid=grid,
        ...    min_n_feat_step=1
        ... )
        >>> # Generazione del report
        >>> fe.make_report()

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
            <table border="0" class="jupyter-style-table">  <thead>    <tr style="text-align: right;">      <th></th>      <th>n_feat</th>      <th>train_score</th>      <th>valid_score</th>      <th>n_feat_to_remove</th>      <th>feat_used</th>      <th>feat_to_remove</th>      <th>feat_select</th>      <th>best_estimator</th>    </tr>  </thead>  <tbody>    <tr>      <th>0</th>      <td>5</td>      <td>0.964706</td>      <td>0.891667</td>      <td>1</td>      <td>[feature3, feature5, feature1, feature2, feature4]</td>      <td>[feature3]</td>      <td>[feature5, feature1, feature2, feature4]</td>      <td>LogisticRegression(C=0.1)</td>    </tr>    <tr>      <th>1</th>      <td>4</td>      <td>0.964706</td>      <td>0.891667</td>      <td>1</td>      <td>[feature4, feature5, feature2, feature1]</td>      <td>[feature4]</td>      <td>[feature5, feature2, feature1]</td>      <td>LogisticRegression(C=0.1)</td>    </tr>    <tr>      <th>2</th>      <td>3</td>      <td>0.982353</td>      <td>0.925000</td>      <td>1</td>      <td>[feature2, feature5, feature1]</td>      <td>[feature2]</td>      <td>[feature5, feature1]</td>      <td>LogisticRegression(C=1)</td>    </tr>    <tr>      <th>3</th>      <td>2</td>      <td>0.817647</td>      <td>0.750000</td>      <td>1</td>      <td>[feature1, feature5]</td>      <td>[feature1]</td>      <td>[feature5]</td>      <td>LogisticRegression(C=0.1)</td>    </tr>    <tr>      <th>4</th>      <td>1</td>      <td>0.788235</td>      <td>0.791667</td>      <td>0</td>      <td>[feature5]</td>      <td>[]</td>      <td>[feature5]</td>      <td>LogisticRegression(C=0.1)</td>    </tr>  </tbody></table>

        >>> fe.extract_features()
        ['feature2', 'feature5', 'feature1']

        >>> fe.get_X_reduced()

        .. raw:: html

            <table border="0" class="jupyter-style-table">  <thead>    <tr style="text-align: right;">      <th></th>      <th>feature2</th>      <th>feature5</th>      <th>feature1</th>    </tr>  </thead>  <tbody>    <tr>      <th>0</th>      <td>5</td>      <td>2</td>      <td>1</td>    </tr>    <tr>      <th>1</th>      <td>4</td>      <td>12</td>      <td>2</td>    </tr>    <tr>      <th>2</th>      <td>3</td>      <td>4</td>      <td>3</td>    </tr>    <tr>      <th>3</th>      <td>2</td>      <td>14</td>      <td>4</td>    </tr>    <tr>      <th>4</th>      <td>1</td>      <td>2</td>      <td>5</td>    </tr>    <tr>      <th>5</th>      <td>6</td>      <td>3</td>      <td>6</td>    </tr>    <tr>      <th>6</th>      <td>3</td>      <td>1</td>      <td>7</td>    </tr>    <tr>      <th>7</th>      <td>7</td>      <td>2</td>      <td>8</td>    </tr>    <tr>      <th>8</th>      <td>3</td>      <td>3</td>      <td>9</td>    </tr>    <tr>      <th>9</th>      <td>5</td>      <td>14</td>      <td>2</td>    </tr>    <tr>      <th>10</th>      <td>8</td>      <td>1</td>      <td>3</td>    </tr>    <tr>      <th>11</th>      <td>4</td>      <td>1</td>      <td>1</td>    </tr>    <tr>      <th>12</th>      <td>2</td>      <td>14</td>      <td>3</td>    </tr>    <tr>      <th>13</th>      <td>9</td>      <td>12</td>      <td>6</td>    </tr>    <tr>      <th>14</th>      <td>75</td>      <td>15</td>      <td>43</td>    </tr>    <tr>      <th>15</th>      <td>4</td>      <td>16</td>      <td>2</td>    </tr>    <tr>      <th>16</th>      <td>5</td>      <td>2</td>      <td>4</td>    </tr>    <tr>      <th>17</th>      <td>7</td>      <td>12</td>      <td>6</td>    </tr>    <tr>      <th>18</th>      <td>5</td>      <td>13</td>      <td>3</td>    </tr>    <tr>      <th>19</th>      <td>2</td>      <td>12</td>      <td>2</td>    </tr>    <tr>      <th>20</th>      <td>5</td>      <td>1</td>      <td>6</td>    </tr>    <tr>      <th>21</th>      <td>8</td>      <td>15</td>      <td>3</td>    </tr>    <tr>      <th>22</th>      <td>6</td>      <td>17</td>      <td>2</td>    </tr>    <tr>      <th>23</th>      <td>3</td>      <td>2</td>      <td>6</td>    </tr>    <tr>      <th>24</th>      <td>5</td>      <td>1</td>      <td>3</td>    </tr>    <tr>      <th>25</th>      <td>7</td>      <td>15</td>      <td>2</td>    </tr>    <tr>      <th>26</th>      <td>8</td>      <td>1</td>      <td>5</td>    </tr>  </tbody></table>
        """
        return self.db[self.final_feat]

    def get_db_filtered(self):
        """Restituisce il `DataFrame` originale senza le feature eliminate.

        Rimuove dal `DataFrame` originale (attributo `db`) le colonne corrispondenti alle feature che sono state eliminate durante il processo RFE e memorizzate nell'attributo `_filtered_out_features` dal metodo `extract_features()`. Mantiene tutte le altre colonne originali (inclusi target, sample_col, ecc.).

        Returns:
            `pd.DataFrame`: Il `DataFrame` originale con le colonne delle feature eliminate rimosse.

        Note:
            Assicurarsi di aver eseguito `make_report()` e `extract_features()` prima di chiamare questo metodo per ottenere un risultato significativo.

        **Esempio:**

        >>> import pandas as pd
        >>> from sklearn.linear_model import LogisticRegression
        >>> from cefeste.elimination import FeatureElimination
        >>> # Dati di esempio
        >>> data = pd.DataFrame({
        ... 'feature1': [1,2,3,4,5,6,7,8,9,2,3,1,3,6,43,2,4,6,3,2,6,3,2,6,3,2,5],
        ... 'feature2': [5,4,3,2,1,6,3,7,3,5,8,4,2,9,75,4,5,7,5,2,5,8,6,3,5,7,8],
        ... 'feature3': [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        ... 'feature4': [8,8,8,9,5,3,4,5,6,2,6,8,4,4,4,6,5,7,8,5,9,3,4,7,5,78,8],
        ... 'feature5': [2,12,4,14,2,3,1,2,3,14,1,1,14,12,15,16,2,12,13,12,1,15,17,2,1,15,1],
        ... 'target':   [0,1,0,1,0,0,0,0,0,1,1,1,1,1,1,1,0,1,1,1,0,1,1,0,1,1,1]
        ... })
        >>> # Parametri
        >>> target_col = 'target'
        >>> model = LogisticRegression()
        >>> grid = {'C': [0.1, 1, 10]}
        >>> # Inizializzazione
        >>> fe = FeatureElimination(
        ...    db=data,
        ...    target_col=target_col,
        ...    model=model,
        ...    grid=grid,
        ...    min_n_feat_step=1
        ... )
        >>> # Generazione del report
        >>> fe.make_report()

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
            <table border="0" class="jupyter-style-table">  <thead>    <tr style="text-align: right;">      <th></th>      <th>n_feat</th>      <th>train_score</th>      <th>valid_score</th>      <th>n_feat_to_remove</th>      <th>feat_used</th>      <th>feat_to_remove</th>      <th>feat_select</th>      <th>best_estimator</th>    </tr>  </thead>  <tbody>    <tr>      <th>0</th>      <td>5</td>      <td>0.964706</td>      <td>0.891667</td>      <td>1</td>      <td>[feature3, feature5, feature1, feature2, feature4]</td>      <td>[feature3]</td>      <td>[feature5, feature1, feature2, feature4]</td>      <td>LogisticRegression(C=0.1)</td>    </tr>    <tr>      <th>1</th>      <td>4</td>      <td>0.964706</td>      <td>0.891667</td>      <td>1</td>      <td>[feature4, feature5, feature2, feature1]</td>      <td>[feature4]</td>      <td>[feature5, feature2, feature1]</td>      <td>LogisticRegression(C=0.1)</td>    </tr>    <tr>      <th>2</th>      <td>3</td>      <td>0.982353</td>      <td>0.925000</td>      <td>1</td>      <td>[feature2, feature5, feature1]</td>      <td>[feature2]</td>      <td>[feature5, feature1]</td>      <td>LogisticRegression(C=1)</td>    </tr>    <tr>      <th>3</th>      <td>2</td>      <td>0.817647</td>      <td>0.750000</td>      <td>1</td>      <td>[feature1, feature5]</td>      <td>[feature1]</td>      <td>[feature5]</td>      <td>LogisticRegression(C=0.1)</td>    </tr>    <tr>      <th>4</th>      <td>1</td>      <td>0.788235</td>      <td>0.791667</td>      <td>0</td>      <td>[feature5]</td>      <td>[]</td>      <td>[feature5]</td>      <td>LogisticRegression(C=0.1)</td>    </tr>  </tbody></table>

        >>> fe.extract_features()
        ['feature2', 'feature5', 'feature1']

        >>> fe.get_db_filtered()

        .. raw:: html

            <table border="0" class="jupyter-style-table">  <thead>    <tr style="text-align: right;">      <th></th>      <th>feature1</th>      <th>feature2</th>      <th>feature5</th>      <th>target</th>    </tr>  </thead>  <tbody>    <tr>      <th>0</th>      <td>1</td>      <td>5</td>      <td>2</td>      <td>0</td>    </tr>    <tr>      <th>1</th>      <td>2</td>      <td>4</td>      <td>12</td>      <td>1</td>    </tr>    <tr>      <th>2</th>      <td>3</td>      <td>3</td>      <td>4</td>      <td>0</td>    </tr>    <tr>      <th>3</th>      <td>4</td>      <td>2</td>      <td>14</td>      <td>1</td>    </tr>    <tr>      <th>4</th>      <td>5</td>      <td>1</td>      <td>2</td>      <td>0</td>    </tr>    <tr>      <th>5</th>      <td>6</td>      <td>6</td>      <td>3</td>      <td>0</td>    </tr>    <tr>      <th>6</th>      <td>7</td>      <td>3</td>      <td>1</td>      <td>0</td>    </tr>    <tr>      <th>7</th>      <td>8</td>      <td>7</td>      <td>2</td>      <td>0</td>    </tr>    <tr>      <th>8</th>      <td>9</td>      <td>3</td>      <td>3</td>      <td>0</td>    </tr>    <tr>      <th>9</th>      <td>2</td>      <td>5</td>      <td>14</td>      <td>1</td>    </tr>    <tr>      <th>10</th>      <td>3</td>      <td>8</td>      <td>1</td>      <td>1</td>    </tr>    <tr>      <th>11</th>      <td>1</td>      <td>4</td>      <td>1</td>      <td>1</td>    </tr>    <tr>      <th>12</th>      <td>3</td>      <td>2</td>      <td>14</td>      <td>1</td>    </tr>    <tr>      <th>13</th>      <td>6</td>      <td>9</td>      <td>12</td>      <td>1</td>    </tr>    <tr>      <th>14</th>      <td>43</td>      <td>75</td>      <td>15</td>      <td>1</td>    </tr>    <tr>      <th>15</th>      <td>2</td>      <td>4</td>      <td>16</td>      <td>1</td>    </tr>    <tr>      <th>16</th>      <td>4</td>      <td>5</td>      <td>2</td>      <td>0</td>    </tr>    <tr>      <th>17</th>      <td>6</td>      <td>7</td>      <td>12</td>      <td>1</td>    </tr>    <tr>      <th>18</th>      <td>3</td>      <td>5</td>      <td>13</td>      <td>1</td>    </tr>    <tr>      <th>19</th>      <td>2</td>      <td>2</td>      <td>12</td>      <td>1</td>    </tr>    <tr>      <th>20</th>      <td>6</td>      <td>5</td>      <td>1</td>      <td>0</td>    </tr>    <tr>      <th>21</th>      <td>3</td>      <td>8</td>      <td>15</td>      <td>1</td>    </tr>    <tr>      <th>22</th>      <td>2</td>      <td>6</td>      <td>17</td>      <td>1</td>    </tr>    <tr>      <th>23</th>      <td>6</td>      <td>3</td>      <td>2</td>      <td>0</td>    </tr>    <tr>      <th>24</th>      <td>3</td>      <td>5</td>      <td>1</td>      <td>1</td>    </tr>    <tr>      <th>25</th>      <td>2</td>      <td>7</td>      <td>15</td>      <td>1</td>    </tr>    <tr>      <th>26</th>      <td>5</td>      <td>8</td>      <td>1</td>      <td>1</td>    </tr>  </tbody></table>
        """
        return self.db.drop(columns=self._filtered_out_features)

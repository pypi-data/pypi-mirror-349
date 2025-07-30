"""Classe utilizzata per implementare tecniche di analisi delle feature."""
from cefeste.utils import get_categorical_features, get_numerical_features
import warnings


class FeatureAnalysis:
    """Classe utilizzata per implementare tecniche di analisi delle feature. Classe madre delle classi :class:`~cefeste.elimination.FeatureElimination` e :class:`~cefeste.selection.FeatureSelection`.

    Questa classe contiene al suo interno metodi utilizzati per svolgere analisi sulle feature e gestire gli attributi della classe quali: l'ottenimento di uno o più attributi della classe, la modifica di questi atttributi e un'analisi esplorativa dei dati di base (EDA) del dataset passato come input.
    """

    def __init__(self, db, feat_to_check=None):
        """Inizializza l'oggetto `FeatureAnalysis` con dati e parametri di configurazione.

        Questo costruttore imposta il `DataFrame` da analizzare e le eventuali feature da considerare per l'analisi dei dati.

        Args:
            db (`pd.DataFrame`): `DataFrame` da analizzare.
            feat_to_check (`list`, optional): Lista delle feature da analizzare. Se `None`, vengono utilizzate tutte le colonne. Default: `None`.
        """
        self.db = db
        if feat_to_check is None:
            feat_to_check = db.columns

        self.feat_to_check = feat_to_check
        self.categorical_features = get_categorical_features(
            db[feat_to_check],
        )
        self.numerical_features = get_numerical_features(
            db[feat_to_check],
        )

    def get_params(self, params=None):
        """Restituisce il valore di uno o più attributi della classe.

        (Metodo importato dalla classe :class:`.FeatureAnalysis`)

        Se `params` è specificato, restituisce il valore dell'attributo richiesto altrimenti restituisce un dizionario contenente tutti gli attributi dell'istanza e i loro valori.

        Args:
            params (`str`, optional): Il nome dell'attributo di cui si desidera ottenere il valore. Se `None`, verranno restituiti tutti gli attributi della classe. Default: `None`.

        Returns:
            `dict`/`object`: Il valore dell'attributo richiesto, oppure un dizionario
            di tutti i parametri dell'istanza se `params` è `None`.

        **Esempio:**

        >>> from cefeste import FeatureAnalysis
        >>> #from cefeste.selection import FeatureSelection
        >>> #from cefeste.elimination import FeatureElimination
        >>> import pandas as pd
        >>> data = {'col1': [1, 2], 'col2': ['A', 'B']}
        >>> df = pd.DataFrame(data)
        >>> analyzer = FeatureAnalysis(df)
        >>> #analyzer = FeatureSelection(df)
        >>> #analyzer = FeatureElimination(df)
        >>> analyzer.get_params('db')

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
            <table border="0" class="jupyter-style-table">  <thead>    <tr style="text-align: right;">      <th></th>      <th>col1</th>      <th>col2</th>    </tr>  </thead>  <tbody>    <tr>      <th>0</th>      <td>1</td>      <td>A</td>    </tr>    <tr>      <th>1</th>      <td>2</td>      <td>B</td>    </tr>  </tbody></table>
        """
        if params is None:
            return self.__dict__
        elif params in self.__dict__.keys():
            return self.__dict__[params]
        else:
            raise ValueError(f"Parameters {params} is not a parameter of the class")

    def set_params(self, exceptions=None, **kwargs):
        """Imposta il valore di uno o più attributi della classe.

        (Metodo importato dalla classe :class:`.FeatureAnalysis`)

        Questo metodo permette di modificare gli attributi dell'istanza. È possibile specificare una lista di attributi che non devono essere sovrascritti tramite il parametro `exceptions`. Se si tenta di sovrascrivere un attributo "protetto", verrà emesso un `warning`.

        Args:
            exceptions (`list`, optional): Una lista di stringhe, dove ogni stringa è il nome di un attributo che non può essere sovrascritto. Default: `None`.
            **kwargs: Argomenti chiave-valore dove la chiave è il nome dell'attributo da impostare e il valore è il nuovo valore per quell'attributo.

        **Esempio:**

        >>> from cefeste import FeatureAnalysis
        >>> #from cefeste.selection import FeatureSelection
        >>> #from cefeste.elimination import FeatureElimination
        >>> import pandas as pd
        >>> data = {'col1': [1, 2], 'col2': ['A', 'B']}
        >>> df = pd.DataFrame(data)
        >>> analyzer = FeatureAnalysis(df)
        >>> #analyzer = FeatureSelection(df)
        >>> #analyzer = FeatureElimination(df)
        >>> analyzer.set_params(feat_to_check=['col1'])
        >>> analyzer.feat_to_check
        ['col1']
        >>> analyzer.set_params(exceptions=['db'], db=None) # Tenta di sovrascrivere 'db'
        UserWarning: Il parametro 'db' non può essere sovrascritto.
        """
        if exceptions is None:
            exceptions = []
        for k, v in kwargs.items():
            if k in self.__dict__.keys():
                if k in exceptions:
                    warnings.warn(f"Parameter {k} cannot be overwritten")
                else:
                    self.__dict__[k] = v
            else:
                raise ValueError(f"Parameter {k} is not a parameter of the class")

    def eda(self):
        """Genera un'analisi esplorativa dei dati (EDA) di base.

        (Metodo importato dalla classe :class:`.FeatureAnalysis`)

        Per ogni feature numerica specificata nell'attributo `numerical_features`, calcola statistiche descrittive. Per ogni feature categorica specificata nell'attributo `categorical_features`, calcola il conteggio dei valori unici.

        Returns:
            `dict`: Un dizionario dove le chiavi sono i nomi delle colonne (feature) e i valori sono:

                - Per le feature numeriche: un oggetto `pd.Series` con le statistiche descrittive.
                - Per le feature categoriche: un oggetto `pd.Series` con i conteggi dei valori.

        **Esempio:**

        >>> from cefeste import FeatureAnalysis
        >>> #from cefeste.selection import FeatureSelection
        >>> #from cefeste.elimination import FeatureElimination
        >>> import pandas as pd
        >>> data = {
        ...     'eta': [25, 30, 25, 35, 30, 40],
        ...     'citta': ['Roma', 'Milano', 'Roma', 'Napoli', 'Milano', 'Roma'],
        ...     'punteggio': [10.5, 15.2, 10.5, 12.0, 18.1, 9.0]
        ... }
        >>> df = pd.DataFrame(data)
        >>> analyzer = FeatureAnalysis(df)
        >>> #analyzer = FeatureSelection(df)
        >>> #analyzer = FeatureElimination(df)
        >>> analysis_results = analyzer.eda()
        >>> analysis_results
        {'eta': count     6.000000
         mean     30.833333
         std       5.845226
         min      25.000000
         25%      26.250000
         50%      30.000000
         75%      33.750000
         max      40.000000
         Name: eta, dtype: float64,
         'punteggio': count     6.000000
         mean     12.550000
         std       3.439041
         min       9.000000
         25%      10.500000
         50%      11.250000
         75%      14.400000
         max      18.100000
         Name: punteggio, dtype: float64,
         'citta': Roma      3
         Milano    2
         Napoli    1
         Name: citta, dtype: int64}
        """
        analysis = dict()
        for col in self.numerical_features:
            analysis[col] = self.db[col].describe()
        for col in self.categorical_features:
            analysis[col] = self.db[col].value_counts()
        return analysis

    def __union__(self, attr_name, new_list):
        """It perform the union between the list stored in the attribute named 'attr_name' and 'new_list' and assign the result to the attribute.

        Args:
            attr_name (str): name of the attribute we want to update
            new_list (list): list we want to merge
        """
        old_list = getattr(self, attr_name)
        setattr(self, attr_name, list(set(old_list).union(set(new_list))))

    def __intersection__(self, attr_name, new_list):
        """It perform the inersection between the list stored in the attribute named 'attr_name' and 'new_list' and assign the result to the attribute.

        Args:
            attr_name (str): name of the attribute we want to update
            new_list (list): list we want to intersecate
        """
        old_list = getattr(self, attr_name)
        setattr(self, attr_name, list(set(old_list).intersection(set(new_list))))

"""Modulo contenente classi utilizzate per implementare trasformazioni delle feature."""
from sklearn.base import TransformerMixin, BaseEstimator
import pandas as pd
import numpy as np


class ColumnExtractor(object):
    """Seleziona un sottoinsieme specificato di colonne da un `DataFrame`.

    Questa classe è un semplice trasformatore utilizzato per estrarre colonne specifiche da un `DataFrame pandas`. Viene utilizzato per applicare i risultati di una selezione di feature o per passare solo un sottoinsieme rilevante di feature al passaggio successivo.
    """

    def __init__(self, cols):
        """Inizializza il ColumnExtractor con la lista di colonne da conservare.

        Args:
            cols (`list`): Una lista contenente i nomi delle colonne che si desidera estrarre e mantenere dal DataFrame di input.
        """
        self.cols = cols

    def transform(self, X):
        """Applica la selezione delle colonne al `DataFrame` di input.

        Restituisce un nuovo `DataFrame` contenente solo le colonne specificate durante l'inizializzazione dell'oggetto.

        Args:
            X (`pd.DataFrame`): Il `DataFrame pandas` da cui estrarre le colonne.

        Returns:
            `pd.DataFrame`: Un `DataFrame` contenente solo le colonne specificate nell'attributo `cols`.

        **Esempio:**

        >>> import pandas as pd
        >>> data = {'A': [1, 2], 'B': [3, 4], 'C': [5, 6]}
        >>> df = pd.DataFrame(data)
        >>> extractor = ColumnExtractor(cols=['A', 'C'])
        >>> df_extracted = extractor.transform(df)
        >>> df_extracted

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
                <table border="0" class="jupyter-style-table">  <thead>    <tr style="text-align: right;">      <th></th>      <th>A</th>      <th>C</th>    </tr>  </thead>  <tbody>    <tr>      <th>0</th>      <td>1</td>      <td>5</td>    </tr>    <tr>      <th>1</th>      <td>2</td>      <td>6</td>    </tr>  </tbody></table>
        """
        return X[self.cols]

    def fit(self, X, y=None):
        """Metodo di fit che non esegue alcuna operazione.

        Questo trasformatore non necessita di apprendere nulla dai dati, quindi il metodo `fit` restituisce semplicemente l'istanza stessa.

        Args:
            X (`pd.DataFrame`): I dati di input. Ignorati.
            y (`np.array`/`pd.Series`, optional): La variabile target. Ignorata. Default: `None`.
        """
        return self

    def fit_transform(self, X, y=None):
        """Esegue fit e transform in un unico passaggio.

        Poiché il metodo `fit` non esegue operazioni, questo metodo è equivalente a chiamare direttamente `transform`.

        Args:
            X (`pd.DataFrame`): Il `DataFrame pandas` da cui estrarre le colonne.
            y (`np.array`/`pd.Series`, optional): La variabile target. Ignorata. Default: None.

        Returns:
            `pd.DataFrame`: Un `DataFrame` contenente solo le colonne specificate nell'attributo `cols`.

        **Esempio:**

        >>> import pandas as pd
        >>> data = {'A': [1, 2], 'B': [3, 4], 'C': [5, 6]}
        >>> df = pd.DataFrame(data)
        >>> extractor = ColumnExtractor(cols=['A', 'C'])
        >>> df_extracted = extractor.fit_transform(df)
        >>> df_extracted

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
                <table border="0" class="jupyter-style-table">  <thead>    <tr style="text-align: right;">      <th></th>      <th>A</th>      <th>C</th>    </tr>  </thead>  <tbody>    <tr>      <th>0</th>      <td>1</td>      <td>5</td>    </tr>    <tr>      <th>1</th>      <td>2</td>      <td>6</td>    </tr>  </tbody></table>
        """
        return self.transform(X)


class ColumnRenamer(object):
    """Rinomina le colonne di un `DataFrame` o assegna nomi a un `array NumPy`.

    Questa classe trasforma l'input (che può essere un `array NumPy` o un `DataFrame pandas`) in un `DataFrame pandas` con i nomi delle colonne specificati. È utile in una pipeline, ad esempio dopo trasformatori che restituiscono `array NumPy`, per riassegnare nomi significativi alle colonne prima di ulteriori passaggi che potrebbero dipendere da essi.
    """

    def __init__(self, col_names):
        """Inizializza il ColumnRenamer con la lista dei nuovi nomi di colonna.

        Args:
            col_names (`list`): Una lista di stringhe che rappresentano i nuovi nomi da assegnare alle colonne dell'input. La lunghezza di questa lista deve corrispondere al numero di colonne dell'input che verrà processato dal metodo `transform`.
        """
        self.col_names = col_names

    def transform(self, X):
        """Converte l'input in un `DataFrame pandas` con i nomi di colonna specificati.

        Se l'input `X` è un `array NumPy`, viene convertito in un `DataFrame`. Se `X` è già un `DataFrame`, i suoi nomi di colonna vengono sovrascritti.

        Args:
            X (`np.array`/`pd.DataFrame`): I dati di input. Il numero di colonne in `X` deve corrispondere alla lunghezza dell'attributo `col_names`.

        Returns:
            `pd.DataFrame`: Un `DataFrame pandas` con le colonne rinominate secondo l'attributo `col_names`.

        **Esempio:**

        >>> import pandas as pd
        >>> renamer = ColumnRenamer(col_names=['feature_1', 'feature_2'])
        >>> data = {'A': [1, 2], 'B': [3, 4]}
        >>> df = pd.DataFrame(data)
        >>> df_renamed_from_df = renamer.transform(df) # Sovrascrive i nomi esistenti
        >>> df_renamed_from_df

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
                <table border="0" class="jupyter-style-table">  <thead>    <tr style="text-align: right;">      <th></th>      <th>feature_1</th>      <th>feature_2</th>    </tr>  </thead>  <tbody>    <tr>      <th>0</th>      <td>1</td>      <td>3</td>    </tr>    <tr>      <th>1</th>      <td>2</td>      <td>4</td>    </tr>  </tbody></table>
        """
        if isinstance(X, pd.DataFrame):
            # Se X è un DataFrame, rinomina le colonne
            X.columns = self.col_names
            return X
        elif isinstance(X, np.ndarray):
            # Se X è un array NumPy, crea un nuovo DataFrame
            X = pd.DataFrame(X, columns=self.col_names)
            return X
        else:
            raise TypeError("Input X deve essere un DataFrame pandas o un array NumPy.")

    def fit(self, X, y=None):
        """Metodo di fit che non esegue alcuna operazione.

        Questo trasformatore non necessita di apprendere nulla dai dati, quindi il metodo `fit` restituisce semplicemente l'istanza stessa.

        Args:
            X (`np.array`/`pd.DataFrame`): I dati di input. Ignorati.
            y (`np.array`/`pd.Series`, optional): La variabile target. Ignorata. Default: `None`.
        """
        return self

    def fit_transform(self, X, y=None):
        """Applica la trasformazione di rinomina delle colonne.

        Poiché `fit` non esegue operazioni, questo metodo è equivalente a chiamare direttamente `transform`.

        Args:
            X (`np.array`/`pd.DataFrame`): I dati di input da trasformare.
            y (`np.array`/`pd.Series`, optional): La variabile target. Ignorata. Default: `None`.

        Returns:
            `pd.DataFrame`: Un `DataFrame pandas` con le colonne rinominate.

        **Esempio:**

        >>> import pandas as pd
        >>> renamer = ColumnRenamer(col_names=['feature_1', 'feature_2'])
        >>> data = {'A': [1, 2], 'B': [3, 4]}
        >>> df = pd.DataFrame(data)
        >>> df_renamed_from_df = renamer.fit_transform(df) # Sovrascrive i nomi esistenti
        >>> df_renamed_from_df

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
                <table border="0" class="jupyter-style-table">  <thead>    <tr style="text-align: right;">      <th></th>      <th>feature_1</th>      <th>feature_2</th>    </tr>  </thead>  <tbody>    <tr>      <th>0</th>      <td>1</td>      <td>3</td>    </tr>    <tr>      <th>1</th>      <td>2</td>      <td>4</td>    </tr>  </tbody></table>
        """
        return self.transform(X)


class Categorizer:
    """Converte colonne specificate di un `DataFrame pandas` al tipo 'category'.

    Questo trasformatore identifica le colonne con `dtype` 'object' (o un sottoinsieme specificato di colonne) e le converte al tipo di dati 'category' di `pandas`. Questo può essere utile per ottimizzare l'uso della memoria e per alcuni modelli di machine learning che trattano specificamente le feature categoriche (es. LightGBM, CatBoost) o prima di applicare one-hot encoding.

    """

    def __init__(self, feat_to_check=None):
        """Inizializza il Categorizer.

        Args:
            feat_to_check (list, optional): Una lista di nomi di colonna da considerare per la conversione. Se `None`, tutte le colonne del `DataFrame` passato al metodo `fit` saranno ispezionate per determinare se sono di tipo 'object'. Default: `None`.
        """
        self.feat_to_check = feat_to_check
        self._fitted = False
        return

    def fit(self, X, y=None):
        """Identifica le colonne con `dtype` 'object' da convertire.

        Questo metodo analizza il `DataFrame` `X`. Se l'attributo `feat_to_check` è stato specificato nel costruttore, considera solo quelle colonne. Altrimenti, considera tutte le colonne di `X`. Le colonne identificate come aventi `dtype` 'object' vengono memorizzate internamente per essere utilizzate dal metodo `transform`.

        Args:
            X (`pd.DataFrame`): Il `DataFrame pandas` di input da cui identificare le colonne di tipo 'object'.
            y (`np.array`/`pd.Series`, optional): Ignorato. Default: `None`.
        """
        self._fitted = True
        if self.feat_to_check is None:
            self.feat_to_check = X.columns

        self._cols_to_categorize = [x for x in X[self.feat_to_check].columns if X[x].dtype == "O"]
        return

    def transform(self, X):
        """Converte le colonne identificate al tipo 'category'.

        Le colonne che sono state identificate come 'object' durante il `fit` vengono convertite al tipo 'category' nel `DataFrame` `X`.

        Args:
            X (`pd.DataFrame`): Il `DataFrame pandas` le cui colonne devono essere trasformate.

        Returns:
            `pd.DataFrame`: Il `DataFrame` con le colonne specificate convertite in 'category'.

        Note:
            Il trasformatore deve essere addestrato usando il metodo `fit` prima di poter chiamare `transform`.

        **Esempio:**

        >>> import pandas as pd
        >>> from cefeste.transform import Categorizer
        >>> data = {'col1': ['A', 'B', 'A'], 'col2': [1, 2, 3], 'col3': ['X', 'Y', 'X']}
        >>> df = pd.DataFrame(data)
        >>> df.dtypes
        col1    object
        col2     int64
        col3    object
        dtype: object
        >>> categorizer_all = Categorizer() # Controlla tutte le colonne
        >>> categorizer_all.fit(df)
        >>> df_transformed_all = categorizer_all.transform(df)
        >>> df_transformed_all.dtypes
        col1    category
        col2       int64
        col3    category
        dtype: object
        """
        if not self._fitted:
            raise ValueError("Categorizer not fitted. Run fit method before.")

        for x in self._cols_to_categorize:
            X[x] = X[x].astype("category")

        return X

    def fit_transform(self, X, y=None):
        """Esegue fit e transform in un unico passaggio.

        Identifica le colonne di tipo 'object' nel `DataFrame` `X` e successivamente le converte al tipo 'category'.

        Args:
            X (`pd.DataFrame`): Il `DataFrame pandas` di input.
            y (`np.array`/`pd.Series`, optional): Ignorato. Default: `None`.

        Returns:
            `pd.DataFrame`: Il `DataFrame` con le colonne appropriate convertite in 'category'.

        **Esempio:**

        >>> import pandas as pd
        >>> from cefeste.transform import Categorizer
        >>> data = {'col1': ['A', 'B', 'A'], 'col2': [1, 2, 3], 'col3': ['X', 'Y', 'X']}
        >>> df = pd.DataFrame(data)
        >>> df.dtypes
        col1    object
        col2     int64
        col3    object
        dtype: object
        >>> categorizer_all = Categorizer() # Controlla tutte le colonne
        >>> df_transformed_all = categorizer_all.fit_transform(df)
        >>> df_transformed_all.dtypes
        col1    category
        col2       int64
        col3    category
        dtype: object
        """
        self._fitted = True

        if self.feat_to_check is None:
            self.feat_to_check = X.columns

        self._cols_to_categorize = [x for x in X[self.feat_to_check].columns if X[x].dtype == "O"]

        for x in self._cols_to_categorize:
            X[x] = X[x].astype("category")

        return X


class Dummitizer(BaseEstimator, TransformerMixin):
    """Converte feature specificate in variabili dummy binarie (0 o 1).

    Questo trasformatore crea variabili dummy dove il valore 1 indica che il valore originale della feature era diverso dall'attributo `base_value` specificato (default 0), e 0 altrimenti. È utile per binarizzare feature o per creare indicatori di presenza/assenza rispetto a un valore di riferimento. Può operare su un sottoinsieme di colonne o su tutte le colonne se non specificato.

    Note:
         Questa classe contiene i metodi `get_params` e `set_params` che vengono ereditati direttamente dalla classe padre `BaseEstimator` della libreria scikit-learn.
    """

    def __init__(self, columns=None, base_value=0):
        """Inizializza il Dummitizer.

        Args:
            columns (`list`, optional): Lista dei nomi delle colonne da trasformare. Se `None`, tutte le colonne verranno considerate durante la trasformazione. Default: `None`.
            base_value (`any`, optional): Il valore rispetto al quale confrontare. I valori diversi da `base_value` diventeranno 1, quelli uguali diventeranno 0. Default: 0.
        """
        self.columns = columns
        self.base_value = base_value

    def fit(self, X, y=None):
        """Metodo di fit che non esegue alcuna operazione.

        Questo trasformatore non necessita di apprendere nulla dai dati, quindi il metodo `fit` restituisce semplicemente l'istanza stessa.

        Args:
            X (`np.array`/`pd.DataFrame`): I dati di input. Ignorati.
            y (`np.array`/`pd.Series`, optional): La variabile target. Ignorata. Default: `None`.
        """
        return self

    def transform(self, X):
        """Applica la trasformazione dummy alle colonne selezionate.

        Per ogni colonna specificata (o tutte se l'attributo `columns` è None), i valori vengono confrontati con l'attributo `base_value`. Se un valore è diverso, viene mappato a 1, altrimenti a 0.

        Args:
            X (`pd.DataFrame`): Il `DataFrame pandas` da trasformare.

        Returns:
            `pd.DataFrame`: Il `DataFrame` con le colonne specificate trasformate in dummy binarie.

        **Esempio:**

        >>> import pandas as pd
        >>> from cefeste.transform import Dummitizer
        >>> data = {'A': [0, 1, 0, 5], 'B': ['x', 'y', 'x', 'z'], 'C': [0, 0, 0, 0]}
        >>> df = pd.DataFrame(data)
        >>> dummitizer_all_base_x = Dummitizer(base_value='x', columns=['B'])
        >>> df_transformed_all = dummitizer_all_base_x.transform(df)
        >>> df_transformed_all

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
                <table border="0" class="jupyter-style-table">  <thead>    <tr style="text-align: right;">      <th></th>      <th>A</th>      <th>B</th>      <th>C</th>    </tr>  </thead>  <tbody>    <tr>      <th>0</th>      <td>0</td>      <td>0</td>      <td>0</td>    </tr>    <tr>      <th>1</th>      <td>1</td>      <td>1</td>      <td>0</td>    </tr>    <tr>      <th>2</th>      <td>0</td>      <td>0</td>      <td>0</td>    </tr>    <tr>      <th>3</th>      <td>5</td>      <td>1</td>      <td>0</td>    </tr>  </tbody></table>
        """
        columns = self.columns
        if self.columns is None:
            columns = X.columns
        X_copy = X.copy()
        X_copy[columns] = (X_copy[columns] != self.base_value).astype("int")
        return X_copy

    def fit_transform(self, X, y=None):
        """Esegue fit e transform in un unico passaggio.

        Poiché `fit` non esegue operazioni, questo metodo è equivalente a chiamare direttamente `transform`.

        Args:
            X (`np.array`/`pd.DataFrame`): I dati di input da trasformare.
            y (`np.array`/`pd.Series`, optional): La variabile target. Ignorata. Default: `None`.

        Returns:
            `pd.DataFrame`: Un `DataFrame pandas` con le colonne rinominate.

        **Esempio:**

        >>> import pandas as pd
        >>> from cefeste.transform import Dummitizer
        >>> data = {'A': [0, 1, 0, 5], 'B': ['x', 'y', 'x', 'z'], 'C': [0, 0, 0, 0]}
        >>> df = pd.DataFrame(data)
        >>> dummitizer_all_base_x = Dummitizer(base_value='x', columns=['B'])
        >>> df_transformed_all = dummitizer_all_base_x.fit_transform(df)
        >>> df_transformed_all

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
                <table border="0" class="jupyter-style-table">  <thead>    <tr style="text-align: right;">      <th></th>      <th>A</th>      <th>B</th>      <th>C</th>    </tr>  </thead>  <tbody>    <tr>      <th>0</th>      <td>0</td>      <td>0</td>      <td>0</td>    </tr>    <tr>      <th>1</th>      <td>1</td>      <td>1</td>      <td>0</td>    </tr>    <tr>      <th>2</th>      <td>0</td>      <td>0</td>      <td>0</td>    </tr>    <tr>      <th>3</th>      <td>5</td>      <td>1</td>      <td>0</td>    </tr>  </tbody></table>
        """
        return self.transform(X)


class ManageOutlier(BaseEstimator, TransformerMixin):
    """Gestisce gli outlier in feature numeriche tramite capping basato sull'IQR.

    Questo trasformatore identifica gli outlier utilizzando il metodo dell'Interquartile Range (IQR). I valori che cadono al di fuori di `Q1 - iqr_multiplier * IQR` o al di sopra di `Q3 + iqr_multiplier * IQR` vengono "cappati", cioè sostituiti con il valore del limite stesso. Può operare su un sottoinsieme di colonne o su tutte le colonne numeriche se non specificato.

    Note:
        -  Questa classe contiene i metodi `get_params` e `set_params` che vengono ereditati direttamente dalla classe padre `BaseEstimator`.
    """

    def __init__(self, columns=None, left_quantile=0.25, right_quantile=0.75, iqr_multiplier=1.5, side="both"):
        """Inizializza il ManageOutlier.

        Args:
            columns (`list`, optional): Colonne su cui operare. Se None, tutte le colonne (numeriche) del `DataFrame` passato come input al metodo `fit`. Default: `None`.
            left_quantile (`float`, optional): Quantile per Q1. Default: 0.25.
            right_quantile (`float`, optional): Quantile per Q3. Default: 0.75.
            iqr_multiplier (`float`, optional): Coefficiente che viene utilizzato come moltiplicatore IQR. Default: 1.5.
            side (`str`, optional): Lato per la gestione degli outlier. Può essere 'both', 'upper', 'lower'. Default: 'both'.
        """
        self.columns = columns
        self.iqr_multiplier = iqr_multiplier
        self.side = side
        self.manage_upper = True
        self.manage_lower = True
        self.left_quantile = left_quantile
        self.right_quantile = right_quantile
        if side == "upper":
            self.manage_lower = False
        elif side == "lower":
            self.manage_upper = False

    def fit(self, X, y=None):
        """Calcola i limiti superiori e inferiori basati sull'IQR dei dati del dataset passato come input.

        I limiti vengono calcolati per ciascuna delle colonne specificate (o per tutte le colonne se l'attributo `columns` è `None`).

        Args:
            X (`pd.DataFrame`): Il `DataFrame pandas` di input (preferibilmente con feature numeriche) utilizzato per calcolare i quantili e i limiti degli outlier.
            y (`np.array`/`pd.Series`, optional): Ignorato. Default: `None`.
        """
        columns = self.columns
        if self.columns is None:
            columns = X.columns

        X_copy = X.copy()[columns]
        q1 = X_copy.quantile(self.left_quantile)
        q3 = X_copy.quantile(self.right_quantile)
        iqr = q3 - q1
        self.upper_lim = np.inf
        self.lower_lim = -np.inf
        if self.manage_upper:
            self.upper_lim = q3 + self.iqr_multiplier * iqr
        if self.manage_lower:
            self.lower_lim = q1 - self.iqr_multiplier * iqr

        return self

    def transform(self, X):
        """Applica il capping degli outlier alle colonne specificate.

        I valori nelle colonne vengono "clippati" (limitati) ai limiti inferiori e superiori calcolati durante il `fit`.

        Args:
            X (`pd.DataFrame`): Il `DataFrame pandas` da trasformare.

        Returns:
            `pd.DataFrame`: Il `DataFrame` con gli outlier cappati nelle colonne specificate.

        **Esempio:**

        >>> import pandas as pd
        >>> from cefeste.transform import ManageOutlier
        >>> data = {'A': [1.1, 1.2, -12, -1.3], 'B': [20, 25, 100, 21]}
        >>> df = pd.DataFrame(data)
        >>> outlier_manager = ManageOutlier(columns=['A', 'B'], iqr_multiplier=0.5, side='both')
        >>> outlier_manager.fit(df)
        >>> df_fitted = outlier_manager.transform(df)
        >>> df_fitted

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
                <table border="0" class="jupyter-style-table">  <thead>    <tr style="text-align: right;">      <th></th>      <th>A</th>      <th>B</th>    </tr>  </thead>  <tbody>    <tr>      <th>0</th>      <td>1.100</td>      <td>20.00</td>    </tr>    <tr>      <th>1</th>      <td>1.200</td>      <td>25.00</td>    </tr>    <tr>      <th>2</th>      <td>-6.525</td>      <td>55.25</td>    </tr>    <tr>      <th>3</th>      <td>-1.300</td>      <td>21.00</td>    </tr>  </tbody></table>
        """
        columns = self.columns
        if self.columns is None:
            columns = X.columns
        X_copy = X.copy()
        X_copy[columns] = X_copy[columns].clip(lower=self.lower_lim, upper=self.upper_lim, axis=1)
        return X_copy

    def fit_transform(self, X, y=None):
        """Esegue fit e transform in un unico passaggio.

        Calcola i limiti degli outlier e successivamente applica il capping.

        Args:
            X (`pd.DataFrame`): Il `DataFrame pandas` di input.
            y (`np.array`/`pd.Series`, optional): Ignorato. Default: `None`.

        Returns:
            `pd.DataFrame`: Il `DataFrame` con gli outlier gestiti.

        **Esempio:**

        >>> import pandas as pd
        >>> from cefeste.transform import ManageOutlier
        >>> data = {'A': [1.1, 1.2, -12, -1.3], 'B': [20, 25, 100, 21]}
        >>> df = pd.DataFrame(data)
        >>> outlier_manager = ManageOutlier(columns=['A', 'B'], iqr_multiplier=0.5, side='both')
        >>> df_fitted = outlier_manager.fit_transform(df)
        >>> df_fitted

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
                <table border="0" class="jupyter-style-table">  <thead>    <tr style="text-align: right;">      <th></th>      <th>A</th>      <th>B</th>    </tr>  </thead>  <tbody>    <tr>      <th>0</th>      <td>1.100</td>      <td>20.00</td>    </tr>    <tr>      <th>1</th>      <td>1.200</td>      <td>25.00</td>    </tr>    <tr>      <th>2</th>      <td>-6.525</td>      <td>55.25</td>    </tr>    <tr>      <th>3</th>      <td>-1.300</td>      <td>21.00</td>    </tr>  </tbody></table>
        """
        return self.fit(X).transform(X)


class LogTransformer(BaseEstimator, TransformerMixin):
    """Applica una trasformazione logaritmica a feature numeriche specificate.

    Questo trasformatore calcola il logaritmo dei valori nelle colonne selezionate, utilizzando una base specificata (default base 10). È comunemente usato per gestire distribuzioni di dati asimmetriche (skewed) o per ridurre l'impatto di ordini di grandezza molto diversi tra le feature.

    Note:
        - La trasformazione logaritmica è definita solo per valori positivi. L'utente deve assicurarsi che le colonne da trasformare contengano valori appropriati (es. > 0). Se sono presenti zeri o valori negativi, potrebbe essere necessario un pre-processing. Questa classe non gestisce automaticamente tali casi.
        -  Questa classe contiene i metodi `get_params` e `set_params` che vengono ereditati direttamente dalla classe padre `BaseEstimator`.
    """

    def __init__(self, columns=None, log_base=10):
        """Inizializza il LogTransformer.

        Args:
            columns (`list`, optional): Colonne su cui applicare il logaritmo. Se `None`, tutte le colonne in `transform`. Default: `None`.
            log_base (`int`/`float`, optional): Base del logaritmo. Default: 10.
        """
        self.columns = columns
        self.log_base = log_base

    def fit(self, X, y=None):
        """Metodo di fit che non esegue alcuna operazione.

        Questo trasformatore non necessita di apprendere nulla dai dati, quindi il metodo `fit` restituisce semplicemente l'istanza stessa.

        Args:
            X (`np.array`/`pd.DataFrame`): I dati di input. Ignorati.
            y (`np.array`/`pd.Series`, optional): La variabile target. Ignorata. Default: `None`.
        """
        return self

    def transform(self, X):
        """Applica la trasformazione logaritmica alle colonne specificate.

        Args:
            X (`pd.DataFrame`): Il `DataFrame pandas` da trasformare. Le colonne selezionate dovrebbero contenere valori positivi.

        Returns:
            `pd.DataFrame`: Un `DataFrame` contenente le colonne trasformate.

        **Esempio:**

        >>> import pandas as pd
        >>> import numpy as np
        >>> from cefeste.transform import LogTransformer
        >>> data = {'A': [1, 10, 100, 1000], 'B': [2, 20, 200, 2000]}
        >>> df = pd.DataFrame(data)
        >>> log_transformer_all_e = LogTransformer(log_base=np.e) # Log naturale su tutte
        >>> df_transformed_all = log_transformer_all_e.transform(df)
        >>> df_transformed_all

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
                <table border="0" class="jupyter-style-table">  <thead>    <tr style="text-align: right;">      <th></th>      <th>A</th>      <th>B</th>    </tr>  </thead>  <tbody>    <tr>      <th>0</th>      <td>0.000000</td>      <td>0.693147</td>    </tr>    <tr>      <th>1</th>      <td>2.302585</td>      <td>2.995732</td>    </tr>    <tr>      <th>2</th>      <td>4.605170</td>      <td>5.298317</td>    </tr>    <tr>      <th>3</th>      <td>6.907755</td>      <td>7.600902</td>    </tr>  </tbody></table>
        """
        columns = self.columns
        if self.columns is None:
            columns = X.columns
        X_copy = X.copy()
        X_copy[columns] = np.log(X_copy[columns]) / np.log(self.log_base)
        return X_copy

    def fit_transform(self, X, y=None):
        """Esegue fit e transform in un unico passaggio.

        Poiché `fit` non esegue operazioni, questo metodo è equivalente a chiamare direttamente `transform`.

        Args:
            X (`np.array`/`pd.DataFrame`): I dati di input da trasformare.
            y (`np.array`/`pd.Series`, optional): La variabile target. Ignorata. Default: `None`.

        Returns:
            `pd.DataFrame`: Un `DataFrame pandas` con le colonne trasformate.

        **Esempio:**

        >>> import pandas as pd
        >>> import numpy as np
        >>> from cefeste.transform import LogTransformer
        >>> data = {'A': [1, 10, 100, 1000], 'B': [2, 20, 200, 2000]}
        >>> df = pd.DataFrame(data)
        >>> log_transformer_all_e = LogTransformer(log_base=np.e) # Log naturale su tutte
        >>> df_transformed_all = log_transformer_all_e.fit_transform(df)
        >>> df_transformed_all

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
                <table border="0" class="jupyter-style-table">  <thead>    <tr style="text-align: right;">      <th></th>      <th>A</th>      <th>B</th>    </tr>  </thead>  <tbody>    <tr>      <th>0</th>      <td>0.000000</td>      <td>0.693147</td>    </tr>    <tr>      <th>1</th>      <td>2.302585</td>      <td>2.995732</td>    </tr>    <tr>      <th>2</th>      <td>4.605170</td>      <td>5.298317</td>    </tr>    <tr>      <th>3</th>      <td>6.907755</td>      <td>7.600902</td>    </tr>  </tbody></table>
        """
        return self.transform(X)

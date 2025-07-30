import os
import shutil
import logging


def copy_replacement_html(app, exception):
    """Copia il contenuto di get e set custom in get e set auto generati dopo la build."""
    original_path = os.path.join(app.confdir, "../build/modules/cefeste.transform/cefeste.transform.Dummitizer.html")
    replacement_path = os.path.join(app.confdir, "../build/html_statici/Dummitizer.html")

    if os.path.exists(original_path) and os.path.exists(replacement_path):
        try:
            shutil.copyfile(replacement_path, original_path)
            logging.info(f"Sostituito il contenuto di {original_path} con {replacement_path}")  # Usa logging.info
        except Exception as e:
            print(f"Errore durante la sostituzione del file: {type(e).__name__}: {e}")

    original_path = os.path.join(app.confdir, "../build/modules/cefeste.transform/cefeste.transform.ManageOutlier.html")
    replacement_path = os.path.join(app.confdir, "../build/html_statici/ManageOutlier.html")

    if os.path.exists(original_path) and os.path.exists(replacement_path):
        try:
            shutil.copyfile(replacement_path, original_path)
            logging.info(f"Sostituito il contenuto di {original_path} con {replacement_path}")  # Usa logging.info
        except Exception as e:
            print(f"Errore durante la sostituzione del file: {type(e).__name__}: {e}")

    original_path = os.path.join(
        app.confdir, "../build/modules/cefeste.transform/cefeste.transform.LogTransformer.html"
    )
    replacement_path = os.path.join(app.confdir, "../build/html_statici/LogTransformer.html")

    if os.path.exists(original_path) and os.path.exists(replacement_path):
        try:
            shutil.copyfile(replacement_path, original_path)
            logging.info(f"Sostituito il contenuto di {original_path} con {replacement_path}")  # Usa logging.info
        except Exception as e:
            print(f"Errore durante la sostituzione del file: {type(e).__name__}: {e}")

    original_path = os.path.join(
        app.confdir, "../build/modules/cefeste.transform/cefeste.transform.Dummitizer.get_params.html"
    )
    replacement_path = os.path.join(app.confdir, "../build/html_statici/Dummitizer.get_params.html")

    if os.path.exists(original_path) and os.path.exists(replacement_path):
        try:
            shutil.copyfile(replacement_path, original_path)
            logging.info(f"Sostituito il contenuto di {original_path} con {replacement_path}")  # Usa logging.info
        except Exception as e:
            print(f"Errore durante la sostituzione del file: {type(e).__name__}: {e}")

    original_path = os.path.join(
        app.confdir, "../build/modules/cefeste.transform/cefeste.transform.Dummitizer.set_params.html"
    )
    replacement_path = os.path.join(app.confdir, "../build/html_statici/Dummitizer.set_params.html")

    if os.path.exists(original_path) and os.path.exists(replacement_path):
        try:
            shutil.copyfile(replacement_path, original_path)
            logging.info(f"Sostituito il contenuto di {original_path} con {replacement_path}")  # Usa logging.info
        except Exception as e:
            print(f"Errore durante la sostituzione del file: {type(e).__name__}: {e}")

    original_path = os.path.join(
        app.confdir, "../build/modules/cefeste.transform/cefeste.transform.ManageOutlier.set_params.html"
    )
    replacement_path = os.path.join(app.confdir, "../build/html_statici/ManageOutlier.set_params.html")

    if os.path.exists(original_path) and os.path.exists(replacement_path):
        try:
            shutil.copyfile(replacement_path, original_path)
            logging.info(f"Sostituito il contenuto di {original_path} con {replacement_path}")  # Usa logging.info
        except Exception as e:
            print(f"Errore durante la sostituzione del file: {type(e).__name__}: {e}")

    original_path = os.path.join(
        app.confdir, "../build/modules/cefeste.transform/cefeste.transform.ManageOutlier.get_params.html"
    )
    replacement_path = os.path.join(app.confdir, "../build/html_statici/ManageOutlier.get_params.html")

    if os.path.exists(original_path) and os.path.exists(replacement_path):
        try:
            shutil.copyfile(replacement_path, original_path)
            logging.info(f"Sostituito il contenuto di {original_path} con {replacement_path}")  # Usa logging.info
        except Exception as e:
            print(f"Errore durante la sostituzione del file: {type(e).__name__}: {e}")

    original_path = os.path.join(
        app.confdir, "../build/modules/cefeste.transform/cefeste.transform.LogTransformer.set_params.html"
    )
    replacement_path = os.path.join(app.confdir, "../build/html_statici/LogTransformer.set_params.html")

    if os.path.exists(original_path) and os.path.exists(replacement_path):
        try:
            shutil.copyfile(replacement_path, original_path)
            logging.info(f"Sostituito il contenuto di {original_path} con {replacement_path}")  # Usa logging.info
        except Exception as e:
            print(f"Errore durante la sostituzione del file: {type(e).__name__}: {e}")

    original_path = os.path.join(
        app.confdir, "../build/modules/cefeste.transform/cefeste.transform.LogTransformer.get_params.html"
    )
    replacement_path = os.path.join(app.confdir, "../build/html_statici/LogTransformer.get_params.html")

    if os.path.exists(original_path) and os.path.exists(replacement_path):
        try:
            shutil.copyfile(replacement_path, original_path)
            logging.info(f"Sostituito il contenuto di {original_path} con {replacement_path}")  # Usa logging.info
        except Exception as e:
            print(f"Errore durante la sostituzione del file: {type(e).__name__}: {e}")


def setup(app):
    """Setup dell'estensione Sphinx."""
    app.connect("build-finished", copy_replacement_html)

    return {
        "version": "0.1",
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }

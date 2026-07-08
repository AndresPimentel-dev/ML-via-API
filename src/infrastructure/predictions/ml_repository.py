import joblib
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import os

from src.domain.interfaces import PredictionService

###############################################################
#modelo que busca contratos
# 1. Definimos la ruta base como el directorio donde vive este archivo (MLrepository.py)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 2. Construimos las rutas de forma segura usando os.path.join
NLPpreprocessor = joblib.load(os.path.join(BASE_DIR, 'vectorizador_tfidf.pkl'))
NLPmodel = joblib.load(os.path.join(BASE_DIR, 'matriz_secop.pkl'))
dfNLP = pd.read_csv(os.path.join(BASE_DIR, 'dataset_final.csv'))

FNCmodel = joblib.load(os.path.join(BASE_DIR, 'modelo_prediccion_adjudicacion.pkl'))
FNCpreprocessor = joblib.load(os.path.join(BASE_DIR, 'preprocesador_prediccion.pkl'))
dfFNC = pd.read_csv(os.path.join(BASE_DIR, 'datosNLPlimp.csv'), usecols=[
    'nombre_del_procedimiento', 'precio_base', 'valor_total_adjudicacion',
    'tipo_de_contrato', 'subtipo_de_contrato', 'duracion', 'unidad_de_duracion',
    'conteo_de_respuestas_a_ofertas', 'adjudicado'
])
##################################################################

class PredictionProvider(PredictionService):

    def get_contracts(self, company_description: str):
        X_trasformed = NLPpreprocessor.transform([company_description])

        similares = cosine_similarity(X_trasformed, NLPmodel).flatten()
        dfNLP['similaridad'] = similares

        dfNLP_ordenado = dfNLP.sort_values(by='similaridad', ascending=False).head(5)
        ############
        #convertimos el df ordenado en dictionarios
        ##########
        return dfNLP_ordenado.to_dict(orient="records")
    
    def get_win_prediction(self, contract_name: str, budget:float):
        print({"contrato nombre en modelo": contract_name, "budget en moidelo": budget})
        contrato_match = dfFNC[dfFNC['nombre_del_procedimiento'].str.contains(contract_name, case=False, na=False)]
        if contrato_match.empty:
            return {"status": "error",
                    "message": "No se encontró ningún contrato con ese nombre. Intenta con palabras clave más específicas."}
        contrato = contrato_match.iloc[0]
        precio_base_real = contrato['precio_base']
        if budget > precio_base_real:
            return {"status": "error",
                    "message": f"Probabilidad: 0.00%. Tu oferta (${budget:,}) supera el presupuesto máximo oficial del contrato (${precio_base_real:,}). Rechazo automático."}
        if budget <= 0:
            return {"status": "error",
                    "message": "Por favor ingresa una oferta económica válida mayor a 0."}
        datos_simulados = pd.DataFrame([{
            'precio_base': budget, # Reemplazamos el precio base por la propuesta del usuario para medir el impacto financiero
            'duracion_dias': contrato['duracion'],
            'tipo_de_contrato': contrato['tipo_de_contrato'],
            'subtipo_de_contrato': contrato['subtipo_de_contrato'],
            'conteo_de_respuestas_a_ofertas': contrato['conteo_de_respuestas_a_ofertas']}])
    
        datos_preprocesados = FNCpreprocessor.transform(datos_simulados)
        probabilidad = FNCmodel.predict_proba(datos_preprocesados)[0][1]
        relacion_precio = budget / precio_base_real
        if relacion_precio < 0.60:
            probabilidad *= 0.3 # Reduce drásticamente la probabilidad original del modelo
        return {
        "data": {
            "probability": float(probabilidad),  # Convert numpy float to standard python float
            "base_price": float(precio_base_real),
            "user_budget": float(budget),
            "ratio": float(relacion_precio)
        }}
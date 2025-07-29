from src.jaqpot_python_sdk.jaqpot_api_client import JaqpotApiClient

jaqpot_api_client = JaqpotApiClient()

prediction = jaqpot_api_client.qsartoolbox_qsar_model_predict_sync('CC', '111bb39c-c97c-4f54-b1de-327a230a8a0c')

print(prediction)

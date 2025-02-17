from django.shortcuts import render, redirect
from .forms import UploadFileForm
import pandas as pd
from prophet import Prophet
from django.conf import settings
import os
import json

# Create your views here.
def home(request):
    return render(request, 'cashflow/home.html')

def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            saved_file = form.save()
            return redirect('forecast', file_id=saved_file.id)  
    else:
        form = UploadFileForm()
    return render(request, 'cashflow/upload.html', {'form': form})

def forecast_view(request, file_id):
    from .models import TransactionFile
    transaction_file = TransactionFile.objects.get(id=file_id)

    file_path = os.path.join(settings.MEDIA_ROOT, str(transaction_file.file))
    df = pd.read_csv(file_path)

    df.rename(columns={'Date': 'ds', 'Amount': 'y'}, inplace=True)
    df['ds'] = pd.to_datetime(df['ds'])

    model = Prophet()
    model.fit(df)

    future = model.make_future_dataframe(periods=30)
    forecast = model.predict(future)

    # Convert ds from Timestamp -> string
    forecast['ds'] = forecast['ds'].astype(str)

    forecast_data = forecast[['ds','yhat']].tail(30).to_dict('records')
    # Or json.dumps with default=str
    forecast_data_json = json.dumps(forecast_data)  # ds is already string

    print("DEBUG: forecast_data_json =", forecast_data_json)

    context = {
        'forecast_data': forecast_data,
        'forecast_data_json': forecast_data_json
    }
    return render(request, 'cashflow/test_forecast.html', context)


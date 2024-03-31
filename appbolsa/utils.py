from matplotlib.ticker import MaxNLocator
from django.http import FileResponse
from .models import RespostasQuestionarioInicial, CustomUser
import matplotlib.pyplot as plt
from io import BytesIO
from .forms import RespostasQuestionarioInicialForm

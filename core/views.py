from datetime import datetime

from django.shortcuts import render

from django.views.generic import FormView, TemplateView
from pandas import DataFrame

from core.form import UploadFileForm
from core.utils import parse_xml_convert_to_data_frame, analyz_by_data_frame, get_files


class UploadFileView(FormView, TemplateView):
    template_name = "parser/parser.html"
    form_class = UploadFileForm
    success_url = "/"

    def get(self, request, *args, **kwargs):

        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form = UploadFileForm(request.POST)

        context = super().get_context_data()

        if form.is_valid():
            date_start = datetime.strptime(form.data.get("date_start"), "%d-%m-%Y").date()
            date_end = datetime.strptime(form.data.get("date_end"), "%d-%m-%Y").date()
            filename = form.data.get("file_choice")

            file = open(filename, "r")

            data_frame = parse_xml_convert_to_data_frame(file, ["full_name", "start", "end"])
            data_frame: DataFrame = analyz_by_data_frame(data_frame, date_start, date_end)
            if data_frame.empty:
                context["total_timing"] = "За данный период нет данных"
                return render(request, template_name=self.template_name, context=context)

            context["df"] = data_frame.to_html
            context["total_timing"] = data_frame["timing"].sum()

        return render(request, template_name=self.template_name, context=context)


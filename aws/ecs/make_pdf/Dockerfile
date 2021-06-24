FROM public.ecr.aws/lambda/python:3.8
ENV AWS_DEFAULT_REGION ap-northeast-1

RUN yum -y install wget \
 && wget https://github.com/wkhtmltopdf/packaging/releases/download/0.12.6-1/wkhtmltox-0.12.6-1.amazonlinux2.x86_64.rpm \
 && yum -y install ./wkhtmltox-0.12.6-1.amazonlinux2.x86_64.rpm \
 && yum -y install which ipa-gothic-fonts \
 && yum -y install python3-devel postgresql-devel libpqxx-dev gcc \
 && pip install pandas pdfkit psycopg2 \
 && rm wkhtmltox-0.12.6-1.amazonlinux2.x86_64.rpm \
 && yum -y remove wget gcc && rm -rf /var/cache/yum/* && yum clean all \
 && wkhtmltopdf --version
 
COPY make_pdf.py   ./

# CMD [ "python", "make_pdf.py" ]

ENTRYPOINT [ "python", "make_pdf.py"]

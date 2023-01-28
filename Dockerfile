FROM python:3

WORKDIR /app/islands

ADD . .

# RUN pip install pytest

CMD ["sh", "your_script.sh", "tests/utils/grids_files/default_data"]
# CMD ["python3", "-m", "pytest"]
deactivate
Remove-Item -Path ..\MaIDe -Recurse -Force
Remove-Item -Path raw_test -Recurse -Force
python -m venv raw_test
.\raw_test\Scripts\activate
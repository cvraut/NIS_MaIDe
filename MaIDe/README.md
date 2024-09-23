# Notes for MaIDe source code

Shortcut cmd to run Maide [source](https://www.bing.com/search?q=bing+chat&cvid=3135c8fd481f4b1d926e51f7602dc808&gs_lcrp=EgZjaHJvbWUqBggBEAAYQDIGCAAQRRg5MgYIARAAGEAyBggCEC4YQDIGCAMQABhAMgYIBBAAGEAyBggFEAAYQDIGCAYQABhAMgYIBxAAGEAyBggIEAAYQDIICAkQ6QcY_FXSAQgyODY3ajBqMagCALACAA&FORM=ANSAB1&PC=HCTS&showconv=1)

`C:\Windows\System32\cmd.exe /k D:\spelioteslab\craut\python.exe D:\spelioteslab\craut\NIS_MaIDe\run.py`

code organization:
- settings.py is outside main directory
- core logic is in `MaIDe.py`
- functions and abstracted logic are in other modules
  - `db.py`
  - `folder_selector.py`
  - `globals.py`
  - `greetings.py`
  - `mac.py`
  - `MaIDe.py`
  - `monitor.py`

# known issues
- dependency installer is broken [permalink to commented out import](https://github.com/cvraut/NIS_MaIDe/blob/b7ddb96cb96ebe56fef210429753755bfa007359/MaIDe/globals.py#L6)
  - just use pip to install
    - `numpy`
    - `nd2`
    - `requests`
    - anything I may have forgotten
    - planned fix involves cleaning up project and deploying to pypi to let pip handle updates and dependencies
      - requires public distribution
      - requires redesign with poetry
      - will likely only happen when truly bored
- [resume functionality is broken](https://github.com/cvraut/NIS_MaIDe/issues/1)
  - feature is just disabled for now
- users cannot select multiple folders to run with MaIDe
  - feature request (new)
# notebook-frontend

A Python package distributing Notebook's static assets only, with no Python dependency.

```bash
curl --output jupyterlab-4.4.2-py3-none-any.whl https://files.pythonhosted.org/packages/f6/ae/fbb93f4990b7648849b19112d8b3e7427bbfc9c5cc8fdc6bf14c0e86d104/jupyterlab-4.4.2-py3-none-any.whl
curl --output notebook-7.4.2-py3-none-any.whl https://files.pythonhosted.org/packages/1e/16/d3c36a0b1f6dfcf218add8eaf803bf0473ff50681ac4d51acb7ba02bce34/notebook-7.4.2-py3-none-any.whl
unzip jupyterlab-4.4.2-py3-none-any.whl
unzip notebook-7.4.2-py3-none-any.whl
mkdir -p share/jupyter
cp -r jupyterlab-4.4.2.data/data/share/jupyter/lab share/jupyter
cp -r notebook-7.4.2.data/data/share/jupyter/lab/* share/jupyter/lab
```

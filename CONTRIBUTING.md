# Contributing

## pre-push

```bash
echo "Git pre push hock"

. ./macrobond_data_api_python_env/Scripts/activate
if test $? != 0
then
    echo -e '\033[31mError in git pre push hock - ./macrobond_data_api_python_env/Scripts/activate\033[0m'
    exit 1
fi

echo "python dir"
python -m pip -V

python ./scripts/lint.py
exit_code=$?
if test $exit_code != 0
then
    echo -e '\033[31mError in commit hock - ./scripts/lint.py\033[0m'
fi

deactivate

exit $exit_code

```

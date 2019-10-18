# Author: Marco Barone Belo
# Github: https://github.com/barone-dev/

# Allow this file to be executed and run it with:
# $ chmod +x python_configs/install.sh && ./python_configs/install.sh

timestamp=$(date +%s)
cd ./python_configs
rm -rf .git README.md
test -d "../.old/" || mkdir "../.old/"
mkdir ../.old/python_configs_$timestamp/
echo "Python Configs 1.0.0"
echo "Moving files to your project root folder:"
for file in $(ls -Ap | grep -v /)
do
    test -f "../$file" && mv "../$file" "../.old/python_configs_$timestamp/"
    mv $file ../
    echo "File ${file} moved"
done

echo "Moving folders to your project root folder"
for directory in $(ls -d */)
do
    test -d "../$directory" && mv -rf "../$directory" "../.old/python_configs_$timestamp/"
    mv -rf $directory ../
    echo "Directory ${directory} moved"
done

cd ..
rm -rf install.sh python_configs/

echo "Thank you for using my configs, feel free to make a pull request with cool aditions."
echo ""
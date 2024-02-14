# Steps to follow to run the Validator locally:

## <b>1. Install Visual Studio Code and Python</b>

  If you haven't already installed Visual Studio Code, you can download it from [here](https://code.visualstudio.com/download) and follow the installation instructions for your operating system.
  Same goes for Python, check it out [here](https://www.python.org/downloads/) and follow the recommended steps for installation again. 
## <b>2. Clone the Repository</b>

  Navigate to the top of this GitHub repository.
  Click on the "Code" button and copy the URL.
  <img width="691" alt="image" src="https://github.com/Dumitru8118/Workshop-Excel-Validator/assets/86912887/73588522-a488-4696-be66-604fb5701298">

  Open Visual Studio Code.
  Open the Command Palette by pressing Ctrl+Shift+P (Windows/Linux) or Cmd+Shift+P (Mac).
  Type "Git: Clone" and select it.
  Paste the copied URL and choose a directory to clone the repository into.

## <b>3. Open the Project in Visual Studio Code</b>

Open Visual Studio Code.
Use File > Open Folder to navigate to the directory where you cloned the repository and opened it.
<img width="577" alt="image" src="https://github.com/Dumitru8118/Workshop-Excel-Validator/assets/86912887/c63d61ef-e982-44ba-995e-2f729834916f">

Your project directory should look like the following:

<img width="341" alt="image" src="https://github.com/Dumitru8118/Workshop-Excel-Validator/assets/86912887/53cce703-3b4b-42d9-9c02-736723fb9b45">


## <b>4. Open Terminal in Visual Studio Code</b>

To open the terminal in Visual Studio Code, you can use the shortcut 
* Ctrl + ` (Windows/Linux) 
* Cmd + ` (Mac).
Alternatively, you can use the menu by navigating to Terminal > New Terminal.

## <b>5. Install Dependencies</b>

Navigate to the root directory of the project in the terminal.
Run the following command to install the required dependencies from the requirements.txt file:
Copy code
```
pip install -r requirements.txt
```

## <b>6. Run the Python Script</b>
Once all dependencies are installed, you can run the Python script by executing the following command in the terminal:
Copy code
```
streamlit run frontend.py
```
Replace script_name.py with the name of your Python script.


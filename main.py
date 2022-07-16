import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

import pandas

import os

import yaml


class App(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        #
        # Root window config
        #
        self.parent.title("SRSBA - Spreadsheet Refactoring Software for Busy Administrators")
        self.parent.config(bg="white")
        self.parent.resizable(False, False)
        self.parent.iconPath = "./spreadsheet-icon.ico"
        self.parent.iconbitmap(self.parent.iconPath)
        self.parent.logoPath = "./spreadsheet-icon-100.png"
        self.parent.logoImage = tk.PhotoImage(file=self.parent.logoPath)

        #
        # Main application config
        #
        self.configurationDirectoryName = ".srsba_config"
        self.configurationChoiceVar = tk.IntVar()
        self.inputFilePath = ""
        self.configurationFileFullPath = ""
        self.inputFileColumnsList_GUI = []
        self.templateFileColumnsList_GUI = []
        self.templateFileColumnsList = []
        self.mappingComboBoxVarList = []
        self.replaceValuesColumnComboBoxVarList = []
        self.replaceValuesInitialValueEntryVarList = []
        self.replaceValuesReplacedByValueEntryVarList = []
        self.transformColumnComboBoxVarList = []
        self.transformTransformTypeComboBoxVarList = []
        self.configurationFileComboboxChoice = tk.StringVar()

        # Filters var
        self.filters = []
        self.filterSourceColumnVarList = []
        self.filterComparisonOperatorVarList = []
        self.filterValueVarList = []

        self.comparisonOperatorsList = ["",
                                        "est égal à",
                                        "est différent de",
                                        "est plus grand que",
                                        "est plus petit que",
                                        ]
        self.transformationTypesList = ["",
                                        "Enlever les accents",
                                        "Tout en majuscules",
                                        "Tout en minuscules",
                                        ]

        self.mainFrame = tk.Frame(parent, bg="white")
        self.mainFrame.grid(column=0, row=0)
        self.mainTitleLogoLabel = tk.Label(self.mainFrame, image=self.parent.logoImage, bg="white")
        self.mainTitleLogoLabel.grid(column=0, row=0, columnspan=999, pady=15, padx=100)
        self.mainSubtitleLabel = tk.Label(self.mainFrame,
                                          text="Spreadsheet Refactoring Software for Busy Administrators",
                                          font=("", 12), bg="white", pady=15)
        self.mainSubtitleLabel.grid(row=1, column=0, columnspan=999)

        # Input file import frame
        self.inputFileImportFrame = tk.LabelFrame(self.mainFrame, text="Importation du fichier", padx=10, pady=10,
                                                  bg="white")
        self.inputFileImportFrame.grid(column=0, row=2, columnspan=3, sticky="W", padx=10, pady=10)

        self.inputFileImportDescriptionLabel = tk.Label(self.inputFileImportFrame,
                                                        text="Choisissez ici le fichier source contenant "
                                                             "toutes les données utiles.", bg="white")
        self.inputFileImportDescriptionLabel.grid(row=3, column=0, columnspan=2, sticky="w", pady=3)

        self.inputFileImportButton = tk.Button(self.inputFileImportFrame, text="Ouvrir un fichier", bg="#479e60",
                                               fg="white", command=self.import_file, padx=10, pady=5)
        self.inputFileImportButton.grid(row=4, column=0)

        self.inputFileImportPathLabel = tk.Label(self.inputFileImportFrame, width=55, borderwidth=1, anchor="e",
                                                 relief="sunken")
        self.inputFileImportPathLabel.grid(row=4, column=1, padx=20)

        # Configuration frame
        self.configurationFrame = tk.LabelFrame(self.mainFrame, text="Configuration", bg="white", padx=10, pady=10)
        self.configurationFrame.grid(column=0, row=5, sticky="WE", padx=10, pady=10)

        self.configurationDescriptionLabel = tk.Label(self.configurationFrame, bg="white",
                                                      text="Sélectionnez ici la méthode de configuration",
                                                      wraplength=520,
                                                      justify=tk.LEFT)
        self.configurationDescriptionLabel.grid(column=0, row=0, columnspan=1, sticky="W", pady=10)

        self.configurationSourceRBLoad = tk.Radiobutton(self.configurationFrame,
                                                        text="Charger une configuration", bg="white",
                                                        value=1, variable=self.configurationChoiceVar,
                                                        command=self.update_config)
        self.configurationSourceRBLoad.grid(column=0, row=1, columnspan=1, sticky="W")

        self.configurationSourceRBNew = tk.Radiobutton(self.configurationFrame, text="Nouvelle configuration", value=2,
                                                       variable=self.configurationChoiceVar, bg="white",
                                                       command=self.update_config)
        self.configurationSourceRBNew.grid(column=0, row=2, columnspan=1, sticky="W")

        # Useless, just declaring the widgets so they can be destroyed in the update_config() method
        self.configurationLoadComboBox = ttk.Combobox(self.configurationFrame)
        self.configurationNewButton = tk.Button(self.configurationFrame)

        # Select a radio button
        self.configurationSourceRBLoad.select()
        self.update_config()

        # Negatives
        self.negativeFileFrame = tk.LabelFrame(self.mainFrame, text="Négatif", padx=10, pady=10, bg="white")
        self.negativeFileFrame.grid(column=0, row=6, sticky="W", pady=10, columnspan=2, padx=10)

        self.negativeFileDescriptionLabel = tk.Label(self.negativeFileFrame,
                                                     text="La fonctionnalité de 'négatif' permet "
                                                          "de supprimer du nouveau fichier les lignes se "
                                                          "trouvant "
                                                          "également dans d'anciens fichiers exportés.\n\n"
                                                          "Pour fonctionner, les fichiers ajoutés "
                                                          "ci-dessous doivent avoir un "
                                                          "format strictement identique au fichier "
                                                          "présentement exporté. ",
                                                     justify=tk.LEFT, wraplength=520, bg="white")
        self.negativeFileDescriptionLabel.grid(column=0, row=0, columnspan=3, sticky="W")

        self.negativeDirectoryImportButton = tk.Button(self.negativeFileFrame,
                                                       text="Sélectionner un dossier",
                                                       padx=10, pady=5, fg="white", bg="#479e60",
                                                       command=self.import_directory)
        self.negativeDirectoryImportButton.grid(row=2, column=0, pady=10, padx=10)

        self.negativeDirectoryPathLabel = tk.Label(self.negativeFileFrame, width=47, borderwidth=1,
                                                   anchor="e",
                                                   relief="sunken")
        self.negativeDirectoryPathLabel.grid(row=2, column=1, padx=20)

        # Final export
        self.finalExportButton = tk.Button(self.mainFrame, text="Exporter", font=("", 12), pady=10, padx=15, fg="white",
                                           bg="#386384")
        self.finalExportButton.grid(column=0, row=7, columnspan=999, padx=25, pady=30)

        #
        # Footer
        #

        footerLabel = tk.Label(self.parent, text="SRSBA - Spreadsheet Refactoring Software for Busy Administrators - v0.2 - dev@strobe.be",
                               bg="lightgrey", fg="black", font=("", 7))
        footerLabel.grid(column=0, row=999, columnspan=6, sticky=tk.W + tk.E)

    def import_file(self):
        self.inputFilePath = filedialog.askopenfilename()

        if self.inputFilePath != "":
            # Add path to the label on the right of the button
            self.inputFileImportPathLabel.configure(text=self.inputFilePath)

            # Detect file type; goal is to support excel, libreoffice and CSV
            fileExtension = self.inputFilePath.split(".")[-1].lower()

            if fileExtension == "csv":
                self.inputFileDataframe = pandas.read_csv(self.inputFilePath, sep=";")

            elif fileExtension == "xlsx" or fileExtension == "xls" or fileExtension == "ods":
                self.inputFileDataframe = pandas.read_excel(self.inputFilePath, sheet_name=0)

            else:
                print("Error: file type not supported")

        else:
            self.inputFileImportPathLabel.configure(text="")

        # Extracting first row to create a list
        self.inputFileColumnsList = list(self.inputFileDataframe.columns)
        self.inputFileColumnsList_GUI = self.inputFileColumnsList.copy()
        self.inputFileColumnsList_GUI.insert(0, "")

    def import_template_file(self):
        self.templateFilePath = filedialog.askopenfilename()

        if self.templateFilePath != "":
            # Add path to the label on the right of the button
            self.templateFileImportPathLabel.configure(text=self.templateFilePath)

            # Detect file type; goal is to support excel, libreoffice and CSV
            fileExtension = self.templateFilePath.split(".")[-1].lower()

            if fileExtension == "csv":
                self.templateFileDataframe = pandas.read_csv(self.templateFilePath, sep=";")

            elif fileExtension == "xlsx" or fileExtension == "xls" or fileExtension == "ods":
                self.templateFileDataframe = pandas.read_excel(self.templateFilePath, sheet_name=0)

            else:
                print("Error: file type not supported")
        else:
            self.templateFileImportPathLabel.configure(text="")

        # Extracting first row to create a list and add a "nothing" value to the GUI list (so user can choose "nothing")
        self.templateFileColumnsList = list(self.templateFileDataframe.columns)
        self.templateFileColumnsList_GUI = self.templateFileColumnsList.copy()
        self.templateFileColumnsList_GUI.insert(0, "")

        # Updating other widgets depending on the templateFileColumnsList list
        self.update_config_mapping()
        self.update_transforms()
        self.update_replace_values()

    def update_transforms(self):
        self.transformFrame.destroy()

        self.transformFrame = tk.LabelFrame(self.transformTabFrame, text="Transformations", bg="white",
                                            padx=10, pady=10)
        self.transformFrame.grid(column=1, row=0, columnspan=1, rowspan=2, padx=10, pady=10, sticky="NW")

        self.transformDescriptionLabel = tk.Label(self.transformFrame, text="Ajoutez des transformations aux "
                                                                            "colonnes que vous voulez.", bg="white")
        self.transformDescriptionLabel.grid(column=0, row=0, columnspan=3, sticky="W", pady=10, padx=10)

        self.transformColumnLabel = tk.Label(self.transformFrame, text="Colonne à modifier", bg="white")
        self.transformColumnLabel.grid(column=0, row=1, padx=5, pady=5)
        self.transformTransformTypeLabel = tk.Label(self.transformFrame, text="Type de transformation",
                                                    bg="white")
        self.transformTransformTypeLabel.grid(column=1, row=1)

        for i in range(0, 10):
            transformColumnComboBoxVar = tk.StringVar()
            transformTransformTypeComboBoxVar = tk.StringVar()

            self.transformColumnComboBox = ttk.Combobox(self.transformFrame, values=self.templateFileColumnsList_GUI,
                                                        state="readonly", width=40,
                                                        textvariable=transformColumnComboBoxVar)
            self.transformColumnComboBox.grid(column=0, row=2 + i, padx=5, pady=5)

            self.transformTransformTypeComboBox = ttk.Combobox(self.transformFrame, values=self.transformationTypesList,
                                                               state="readonly", width=40,
                                                               textvariable=transformTransformTypeComboBoxVar)
            self.transformTransformTypeComboBox.grid(column=1, row=2 + i, padx=5, pady=5)

            self.transformColumnComboBoxVarList.insert(i, transformColumnComboBoxVar)
            self.transformTransformTypeComboBoxVarList.insert(i, transformTransformTypeComboBoxVar)

    def update_replace_values(self):
        self.replaceValuesFrame.destroy()

        self.replaceValuesFrame = tk.LabelFrame(self.replaceValuesTabFrame, text="Remplacer des valeurs "
                                                                                 "par d'autres", bg="white",
                                                padx=10)
        self.replaceValuesFrame.grid(column=1, row=2, columnspan=1, padx=10, pady=10, sticky="NW")

        self.replaceValuesDescriptionLabel = tk.Label(self.replaceValuesFrame, text="Remplacez une valeur par une "
                                                                                    "autre dans une colonne "
                                                                                    "précise.", bg="white")
        self.replaceValuesDescriptionLabel.grid(column=0, row=0, columnspan=3, padx=10, pady=10, sticky="W")

        self.replaceValuesColumnLabel = tk.Label(self.replaceValuesFrame, text="Colonne de recherche",
                                                 bg="white")
        self.replaceValuesColumnLabel.grid(column=0, row=1, padx=5, pady=5)
        self.replaceValuesInitialValueLabel = tk.Label(self.replaceValuesFrame, text="Valeur initiale",
                                                       bg="white")
        self.replaceValuesInitialValueLabel.grid(column=1, row=1, padx=5, pady=5)
        self.replaceValuesReplacedByValueLabel = tk.Label(self.replaceValuesFrame, text="Valeur de "
                                                                                        "remplacement",
                                                          bg="white")
        self.replaceValuesReplacedByValueLabel.grid(column=2, row=1, padx=5, pady=5)

        for i in range(0, 10):
            replaceValuesColumnComboBoxVar = tk.StringVar()
            replaceValuesInitialValueEntryVar = tk.StringVar()
            replaceValuesReplacedByValueEntryVar = tk.StringVar()

            self.replaceValuesColumnComboBox = ttk.Combobox(self.replaceValuesFrame,
                                                            values=self.templateFileColumnsList_GUI,
                                                            state="readonly", width=40,
                                                            textvariable=replaceValuesColumnComboBoxVar)
            self.replaceValuesColumnComboBox.grid(column=0, row=2 + i, padx=5, pady=5)

            self.replaceValuesInitialValueEntry = tk.Entry(self.replaceValuesFrame,
                                                           textvariable=replaceValuesInitialValueEntryVar)
            self.replaceValuesInitialValueEntry.grid(column=1, row=2 + i, padx=5, pady=5)

            self.replaceValuesReplacedByValueEntry = tk.Entry(self.replaceValuesFrame,
                                                              textvariable=replaceValuesReplacedByValueEntryVar)
            self.replaceValuesReplacedByValueEntry.grid(column=2, row=2 + i, padx=5, pady=5)

            self.replaceValuesColumnComboBoxVarList.insert(i, replaceValuesColumnComboBoxVar)
            self.replaceValuesInitialValueEntryVarList.insert(i, replaceValuesInitialValueEntryVar)
            self.replaceValuesReplacedByValueEntryVarList.insert(i, replaceValuesReplacedByValueEntryVar)

    def import_directory(self):
        self.negativeDirectoryPath = filedialog.askdirectory()

        if self.negativeDirectoryPath != "":
            # Clear lists in case it's not the first imported file

            # Add path to the label on the right of the button
            self.negativeDirectoryPathLabel.configure(text=self.negativeDirectoryPath)
        else:
            self.negativeDirectoryPathLabel.configure(text="")

    def update_config(self):
        if self.configurationChoiceVar.get() == 1:

            # Look for configuration files
            self.update_config_files_list()

            self.configurationNewButton.destroy()
            self.configurationLoadComboBox.destroy()
            self.configurationLoadComboBox = ttk.Combobox(self.configurationFrame,
                                                          values=self.configurationFilesList_GUI,
                                                          textvariable=self.configurationFileComboboxChoice,
                                                          width=43, state="readonly")
            self.configurationLoadComboBox.grid(column=1, row=1, rowspan=2, sticky="E", padx=10)

            # Looking at choice made to get the full configuration file path
            # self.configurationFilesList and self.configruationFilesList_GUI share the same index
            for i in range(len(self.configurationFilesList_GUI)):
                if self.configurationFileComboboxChoice.get() != "":
                    if self.configurationFilesList_GUI[i] == self.configurationFileComboboxChoice.get():
                        self.configurationFileFullPath = os.path.expanduser("~") + "/" + \
                                                         self.configurationDirectoryName + "/" + \
                                                         self.configurationFilesList[i]

        elif self.configurationChoiceVar.get() == 2:
            self.configurationLoadComboBox.destroy()
            self.configurationNewButton.destroy()
            self.configurationNewButton = tk.Button(self.configurationFrame, text="Configurer...", bg="#479e60",
                                                    fg="white", command=self.show_configuration_window,
                                                    padx=10, pady=5)
            self.configurationNewButton.grid(column=1, row=1, rowspan=2, sticky="E", padx=103)

    def update_config_files_list(self):
        self.check_config_directory()
        configDirectoryFilesList = os.listdir(os.path.expanduser("~") + "/" + self.configurationDirectoryName)
        self.configurationFilesList_GUI = []  # Special list for the GUI (without the extensions)
        self.configurationFilesList = []

        for file in configDirectoryFilesList:
            if file.split(".")[-1].lower() == "yaml":
                self.configurationFilesList_GUI.append(file.split(".")[-2])
                self.configurationFilesList.append(file)

    def check_config_directory(self):
        if not os.path.isdir(os.path.expanduser("~") + "/" + self.configurationDirectoryName):
            os.mkdir(os.path.expanduser("~") + "/" + self.configurationDirectoryName)

    def show_configuration_window(self):
        self.configurationWindow = tk.Toplevel()
        self.configurationWindow.title("SRSBA - Nouvelle configuration")
        self.configurationWindow.config(bg="white")
        self.configurationWindow.resizable(False, False)
        self.configurationWindow.iconbitmap(self.parent.iconPath)
        self.configurationWindow.grab_set()

        self.configurationWindowMainFrame = tk.Frame(self.configurationWindow, bg="white")
        self.configurationWindowMainFrame.grid(column=0, row=0)

        self.configurationTabs = ttk.Notebook(self.configurationWindow)

        # Filter rows
        self.sourceFileFilterTabFrame = tk.Frame(self.configurationTabs, bg="white")
        self.sourceFileFilterFrame = tk.LabelFrame(self.sourceFileFilterTabFrame, text="Filtrer les données", padx=10,
                                                   pady=10,
                                                   width=533, height=100, bg="white")
        self.sourceFileFilterFrame.grid(column=0, row=2, columnspan=3, sticky="w", padx=10, pady=10)

        filterSourceColumnLabel = tk.Label(self.sourceFileFilterFrame, text="Colonne à filtrer", bg="white")
        filterSourceColumnLabel.grid(column=1, row=0, padx=5, pady=5)
        comparisonOperatorLabel = tk.Label(self.sourceFileFilterFrame, text="Opérateur", bg="white")
        comparisonOperatorLabel.grid(column=2, row=0, pady=5, padx=5)
        filterValueLabel = tk.Label(self.sourceFileFilterFrame, text="Valeur du filtre", bg="white")
        filterValueLabel.grid(column=3, row=0, padx=5, pady=5)

        for i in range(0, 10):
            filterSourceColumnVar = tk.StringVar()
            comparisonOperatorComboboxVar = tk.StringVar()
            filterValueEntry = tk.StringVar()

            if i >= 1:
                self.filterLogicalOperatorLabel = tk.Label(self.sourceFileFilterFrame, text="ET", bg="white")
                self.filterLogicalOperatorLabel.grid(column=0, row=i + 1, columnspan=1, sticky="W")

            filterSourceColumn = ttk.Combobox(self.sourceFileFilterFrame, values=self.inputFileColumnsList_GUI,
                                              width=40, state="readonly", textvariable=filterSourceColumnVar)
            filterSourceColumn.grid(column=1, row=i + 1, padx=5, pady=5)

            comparisonOperatorCombobox = ttk.Combobox(self.sourceFileFilterFrame, values=self.comparisonOperatorsList,
                                                      width=20, state="readonly",
                                                      textvariable=comparisonOperatorComboboxVar)
            comparisonOperatorCombobox.grid(column=2, row=i + 1, padx=5, pady=5)

            filterValueEntry = tk.Entry(self.sourceFileFilterFrame, width=40, textvariable=filterValueEntry)
            filterValueEntry.grid(column=3, row=i + 1, padx=5, pady=5)

            self.filterSourceColumnVarList.insert(i, filterSourceColumnVar)
            self.filterComparisonOperatorVarList.insert(i, comparisonOperatorComboboxVar)
            self.filterValueVarList.insert(i, filterValueEntry)

        # Import template file
        self.importTemplateTab = tk.Frame(self.configurationTabs, bg="white")

        self.templateFileImportFrame = tk.LabelFrame(self.importTemplateTab, text="Importation du modèle", padx=10,
                                                     pady=10,
                                                     bg="white")
        self.templateFileImportFrame.grid(column=0, row=0, columnspan=1, sticky="W", padx=10, pady=10)

        self.templateFileImportDescriptionLabel = tk.Label(self.templateFileImportFrame,
                                                           text="Choisissez ici le fichier modèle au format .csv",
                                                           bg="white")
        self.templateFileImportDescriptionLabel.grid(row=3, column=0, columnspan=2, sticky="w", pady=3)

        self.templateFileImportButton = tk.Button(self.templateFileImportFrame, text="Ouvrir un fichier", bg="#479e60",
                                                  fg="white", command=self.import_template_file, padx=10, pady=5)
        self.templateFileImportButton.grid(row=4, column=0)

        self.templateFileImportPathLabel = tk.Label(self.templateFileImportFrame, width=55, borderwidth=1, anchor="e",
                                                    relief="sunken")
        self.templateFileImportPathLabel.grid(row=4, column=1, padx=20)

        # Mapping
        self.selectRelevantDataTabFrame = tk.Frame(self.configurationTabs, bg="white")
        # Useless, declaration here so it can be destroyed later
        self.selectRelevantDataFrame = tk.LabelFrame(self.selectRelevantDataTabFrame)

        # Transformations
        self.transformTabFrame = tk.Frame(self.configurationTabs, bg="white")
        # Useless, declaration here so it can be destroyed later
        self.transformFrame = tk.LabelFrame(self.transformTabFrame)

        # Replace values
        self.replaceValuesTabFrame = tk.Frame(self.configurationTabs, bg="white")
        # Useless, declaration here so it can be destroyed later
        self.replaceValuesFrame = tk.LabelFrame(self.replaceValuesTabFrame)

        # Save configuration as...
        self.saveConfigurationTabFrame = tk.Frame(self.configurationTabs, bg="white")
        self.saveConfigurationFrame = tk.LabelFrame(self.saveConfigurationTabFrame, text="Sauvegarder la "
                                                                                         "configuration",
                                                    bg="white", padx=10, pady=10)
        self.saveConfigurationFrame.grid(column=0, row=0, columnspan=2, padx=10, pady=10, sticky="NW")

        self.saveConfigurationDescriptionLabel = tk.Label(self.saveConfigurationFrame, text="Sauvegardez la "
                                                                                            "configuration.",
                                                          bg="white")
        self.saveConfigurationDescriptionLabel.grid(column=0, row=0, columnspan=3, padx=10, pady=10, sticky="W")

        self.saveConfigurationNameLabel = tk.Label(self.saveConfigurationFrame, text="Nom de la nouvelle configuration",
                                                   bg="white")
        self.saveConfigurationNameLabel.grid(column=0, row=1, pady=10, padx=10)

        self.saveConfigurationNameEntry = tk.Entry(self.saveConfigurationFrame, width=40)
        self.saveConfigurationNameEntry.grid(column=1, row=1, pady=10, padx=10)

        self.saveConfigurationButton = tk.Button(self.saveConfigurationFrame, text="Enregistrer la configuration",
                                                 bg="#479e60", fg="white", pady=5, padx=10,
                                                 command=self.save_config)
        self.saveConfigurationButton.grid(column=1, row=2, sticky="E", pady=20)

        # Tabs
        self.configurationTabs.add(self.sourceFileFilterTabFrame, text="Filtrer les données")
        self.configurationTabs.add(self.importTemplateTab, text="*Importation du modèle")
        self.configurationTabs.add(self.selectRelevantDataTabFrame, text="*Sélection et mapping")
        self.configurationTabs.add(self.replaceValuesTabFrame, text="Remplacer des valeurs")
        self.configurationTabs.add(self.transformTabFrame, text="Transformations")
        self.configurationTabs.add(self.saveConfigurationTabFrame, text="*Sauvegarder la configuration")
        self.configurationTabs.grid(column=0, row=0, pady=5)

    def update_config_mapping(self):
        self.selectRelevantDataFrame.destroy()

        self.selectRelevantDataFrame = tk.LabelFrame(self.selectRelevantDataTabFrame, text="Sélectionner les données à "
                                                                                           "utiliser",
                                                     padx=10, pady=10, bg="white")
        self.selectRelevantDataFrame.grid(column=0, row=1, sticky="nw", pady=10, padx=10)

        self.canvas = tk.Canvas(self.selectRelevantDataFrame, borderwidth=0, background="#ffffff",
                                width=700, height=400, highlightthickness=0)
        self.frame = tk.Frame(self.canvas, background="#ffffff", borderwidth=0)
        vsb = tk.Scrollbar(self.selectRelevantDataFrame, orient=tk.VERTICAL, command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=vsb.set)

        vsb.grid(column=999, row=0, sticky="NS")
        self.canvas.grid(column=0, row=0, columnspan=6)
        self.canvas.grid_columnconfigure(0, weight=1)
        self.canvas.create_window((4, 4), window=self.frame, anchor="nw")

        self.frame.bind("<Configure>",
                        lambda event, canvas=self.canvas: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        # Show Labels and Combobox with first row values
        for i in range(0, len(self.templateFileColumnsList)):

            mappingComboBoxVar = tk.StringVar()

            if len(self.templateFileColumnsList[i]) > 60:
                templateColumnsLabelContent_GUI = self.templateFileColumnsList[i][:60] + "..."
            else:
                templateColumnsLabelContent_GUI = self.templateFileColumnsList[i]

            templateColumnsLabel = tk.Label(self.frame, text=templateColumnsLabelContent_GUI, bg="white")
            templateColumnsLabel.grid(column=0, row=i, sticky="w", padx=10, pady=5)

            mappingComboBox = ttk.Combobox(self.frame, values=self.inputFileColumnsList_GUI,
                                           state="readonly", width=40, textvariable=mappingComboBoxVar)
            mappingComboBox.grid(column=1, row=i, sticky="w", padx=10, pady=5)

            self.mappingComboBoxVarList.insert(i, mappingComboBoxVar)

    def save_config(self):
        self.get_config()

        if self.saveConfigurationNameEntry.get() != "":
            configFile = open(os.path.expanduser("~") + "/" + self.configurationDirectoryName + "/" +
                              self.saveConfigurationNameEntry.get() + ".yaml", 'w')

            yaml.safe_dump(self.finalConfig, configFile)

            self.configurationWindow.destroy()

        else:
            print("Erreur: Pas de nom pour la configuration !")

    def get_config(self):
        # Get the config; contains all relevant lists to be saved inside a configuration file

        # Fetch filters values
        self.filters = []
        for i in range(len(self.filterSourceColumnVarList)):  # Way to go through all the settings
            if self.filterSourceColumnVarList[i].get() != "":
                setting_row = [self.filterSourceColumnVarList[i].get(), self.filterComparisonOperatorVarList[i].get(),
                               self.filterValueVarList[i].get()]
                self.filters.append(setting_row)

        # Fetch mappings (at this point there should not be any blank fields, check is made earlier)
        self.mappings = []
        for i in range(len(self.templateFileColumnsList)):
            setting_mappings = [self.templateFileColumnsList[i], self.mappingComboBoxVarList[i].get()]
            self.mappings.append(setting_mappings)

        # Fetch replaced values
        self.replacedValues = []
        for i in range(len(self.replaceValuesColumnComboBoxVarList)):
            if self.replaceValuesColumnComboBoxVarList[i].get() != "":
                setting_replacedValues = [self.replaceValuesColumnComboBoxVarList[i].get(),
                                          self.replaceValuesInitialValueEntryVarList[i].get(),
                                          self.replaceValuesReplacedByValueEntryVarList[i].get()]
                self.replacedValues.append(setting_replacedValues)

        # Fetch transformations values
        self.transformations = []
        for i in range(len(self.transformColumnComboBoxVarList)):
            if self.transformColumnComboBoxVarList[i].get() != "":
                setting_transformations = [self.transformColumnComboBoxVarList[i].get(),
                                           self.transformTransformTypeComboBoxVarList[i].get()]
                self.transformations.append(setting_transformations)

        # Method to fetch all relevant settings
        self.finalConfig = {
            "inputFileColumnsName": self.inputFileColumnsList,
            "templateFileColumnsName": self.templateFileColumnsList,

            "filters": self.filters,
            "mappings": self.mappings,
            "replacedValues": self.replacedValues,
            "transformations": self.transformations,
        }


if __name__ == "__main__":
    root = tk.Tk()
    thisApp = App(root)
    thisApp.grid(column=0, row=0)
    root.mainloop()

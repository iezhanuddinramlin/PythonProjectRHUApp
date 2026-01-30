# Name: MUHAMMAD IEZHANUDDIN BIN RAMLIN
# Student ID: 24015892

import sys
from platform import release

from PySide6.QtWidgets import QApplication, QMainWindow, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QLabel, \
    QWidget, \
    QMessageBox, QListView, QStyledItemDelegate, QDialog, QStackedWidget, QGridLayout, QCheckBox, QComboBox
from PySide6.QtCore import Qt, QAbstractListModel, QModelIndex, QSize
from PySide6.QtGui import QPainter

# This class is for generating a custom list model for QListView
class CustomListModel(QAbstractListModel):
    def __init__(self, data):
        super().__init__()
        self._data = data

    def rowCount(self, parent:None):
        return len(self._data)

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            return self._data[index.row()]['name']
        return None

    def flags(self, index):
        return Qt.ItemIsEnabled | Qt.ItemIsSelectable

# This class is for generating delegates to add more colour variations for the QListView
class CustomItemDelegate(QStyledItemDelegate):
    def createEditor(self, parent, option, index):
        # Optionally, create an editor for editing items
        editor = QLabel(parent)
        editor.setAlignment(Qt.AlignLeft)
        return editor

    def paint(self, painter, option, index):
        # Custom painting of the item
        painter.save()
        painter.setRenderHint(QPainter.Antialiasing)

        # Custom item background color based on index
        if index.row() % 2 == 0:
            painter.fillRect(option.rect, Qt.lightGray)
            # Light gray for even rows
        else:
            painter.fillRect(option.rect, Qt.black)
            # White for odd rows

        # Draw the item text
        text = index.data()
        painter.drawText(option.rect, Qt.AlignLeft | Qt.AlignVCenter, text)
        painter.restore()

    def sizeHint(self, option, index):
        # Return the size hint for the item
        return QSize(200, 40)  # Custom size for the items

# This class handles the code for QDialog popup window when adding a new housing unit in the RHU Tab
class AddRHUWindow(QDialog):
    def __init__(self):
        super().__init__()

        pageLayout = QVBoxLayout(self) # Initialise main page layout vertically, self is passed to establish parent-child connection

        headerBar = QWidget()   # Creating the main widget for the window, self is not needed as it has been passed in pageLayout
        headerLayout = QHBoxLayout(headerBar)   # Set its layout so the buttons would appear horizontally (mimic a tab system)

        # Create tab navigation buttons for each page
        basicInfo = QPushButton("Basic Info")
        headerLayout.addWidget(basicInfo)
        basicInfo.clicked.connect(lambda: self.stackWidget.setCurrentIndex(0))  # Implement signal and slots feature to connect buttons to events

        features = QPushButton("Requirements")
        headerLayout.addWidget(features)
        features.clicked.connect(lambda: self.stackWidget.setCurrentIndex(1))

        residentList = QPushButton("Add Notes")
        headerLayout.addWidget(residentList)
        residentList.clicked.connect(lambda: self.stackWidget.setCurrentIndex(2))

        pageLayout.addWidget(headerBar)     # Add the buttons to the headerBar widget so it could appear in the app

        # Implement QStackWidget to store page content, this allows the buttons to interact and change between pages seamlessly
        self.stackWidget = QStackedWidget(self)

        self.basic_info_TabView()   # Create a new function in the same class and put the page code in there to clean up code and ensure readability

        self.stackWidget.addWidget(self.basicInfoPage)

        self.add_notes_TabView()    # Instead of writing hardcoding everything in __init__, I can just call the function.

        self.stackWidget.addWidget(self.addNotesPage)

        self.resident_list_TabView()

        self.stackWidget.addWidget(self.residentListPage)

        pageLayout.addWidget(self.stackWidget)

        # Create a footer bar that houses the QDialog action buttons, delete, cancel and save changes
        footerButtons = QWidget(self)
        footerLayout = QHBoxLayout(footerButtons)

        deleteButton = QPushButton('Delete')
        footerLayout.addWidget(deleteButton)
        deleteButton.clicked.connect(self.close)

        cancelButton = QPushButton('Cancel')
        footerLayout.addWidget(cancelButton)
        cancelButton.clicked.connect(self.close)

        saveChangesButton = QPushButton('Save Changes')
        footerLayout.addWidget(saveChangesButton)
        saveChangesButton.clicked.connect(self.close)

        pageLayout.addWidget(footerButtons)

    # Function that shows the basic info tab page
    def basic_info_TabView(self):
        self.basicInfoPage = QWidget()
        basicInfoPageLayout = QGridLayout(self.basicInfoPage)

        self.RHUName = QLineEdit()
        self.RHUName.setPlaceholderText("Housing Name")
        basicInfoPageLayout.addWidget(self.RHUName, 0, 0)

        self.RHUaddress = QLineEdit()
        self.RHUaddress.setPlaceholderText("Housing Address")
        basicInfoPageLayout.addWidget(self.RHUaddress, 1, 0)

        self.email = QLineEdit()
        self.email.setPlaceholderText("Email")
        basicInfoPageLayout.addWidget(self.email, 2, 0)

        self.management = QComboBox()
        self.management.addItem("Select housing management..")
        self.management.addItem("Commercial")
        self.management.addItem("Charity")
        basicInfoPageLayout.addWidget(self.management, 3, 0)

        self.phone = QLineEdit()
        self.phone.setPlaceholderText("Phone Number")
        basicInfoPageLayout.addWidget(self.phone, 2, 1)

        self.capacity = QLineEdit()
        self.capacity.setPlaceholderText("Housing Capacity")
        basicInfoPageLayout.addWidget(self.capacity, 0, 1)

        self.costPerBed = QLineEdit()
        self.costPerBed.setPlaceholderText("Cost per Bed")
        basicInfoPageLayout.addWidget(self.costPerBed, 1, 1)

    # Function that shows the additional notes tab page
    def add_notes_TabView(self):
        self.addNotesPage = QWidget()
        addNotesPageLayout = QVBoxLayout(self.addNotesPage)

        addNotesLabel = QLabel("Additional Notes for Housing")
        addNotesPageLayout.addWidget(addNotesLabel)

        addNotesField = QLineEdit()
        addNotesField.setPlaceholderText("Enter additional notes here..)")
        addNotesPageLayout.addWidget(addNotesField)

    # Function that shows the list of residents for each housing unit entry in resident list tab page
    def resident_list_TabView(self):
        self.residentListPage = QWidget()
        self.residentListPageLayout = QVBoxLayout(self.residentListPage)

        # Hardcoded data for the QListView
        self.residentList = QListView()
        self.data = [
            {'name': 'Dustin'},
            {'name': 'Johnathan'},
            {'name': 'Hop'},
            {'name': 'Dustin'},
            {'name': 'Johnathan'},
            {'name': 'Hop'},
            {'name': 'Dustin'},
            {'name': 'Johnathan'},
            {'name': 'Hop'},
            {'name': 'Dustin'},
            {'name': 'Johnathan'},
            {'name': 'Hop'},
            {'name': 'Keema'}
        ]

        self.overviewModel = CustomListModel(self.data) # Creating a QListView model using the CustomListModel function for the given data

        self.residentList.setModel(self.overviewModel)

        self.residentList.setItemDelegate(CustomItemDelegate()) # Implementing custom delegates to add colour variations into the list view

        self.residentListPageLayout.addWidget(self.residentList)

# This class handles the code for QDialog popup window when adding a new licencee in the overview tab
class AddLicenceeWindow(QDialog):
    def __init__(self):
        super().__init__()

        pageLayout = QVBoxLayout(self)

        headerBar = QWidget()
        headerLayout = QHBoxLayout(headerBar)

        basicInfo = QPushButton("Basic Info")
        headerLayout.addWidget(basicInfo)
        basicInfo.clicked.connect(lambda: self.stackWidget.setCurrentIndex(0))

        requirements = QPushButton("Requirements")
        headerLayout.addWidget(requirements)
        requirements.clicked.connect(lambda: self.stackWidget.setCurrentIndex(1))

        addNotes = QPushButton("Add Notes")
        headerLayout.addWidget(addNotes)
        addNotes.clicked.connect(lambda: self.stackWidget.setCurrentIndex(2))

        pageLayout.addWidget(headerBar)

        self.stackWidget = QStackedWidget(self)

        self.basic_info_TabView()

        self.stackWidget.addWidget(self.basicInfoPage)

        self.requirements_TabView()

        self.stackWidget.addWidget(self.requirementsPage)

        self.add_notes_TabView()

        self.stackWidget.addWidget(self.addNotesPage)

        pageLayout.addWidget(self.stackWidget)

        footerButtons = QWidget(self)
        footerLayout = QHBoxLayout(footerButtons)

        deleteButton = QPushButton('Delete')
        footerLayout.addWidget(deleteButton)
        deleteButton.clicked.connect(self.close)

        cancelButton = QPushButton('Cancel')
        footerLayout.addWidget(cancelButton)
        cancelButton.clicked.connect(self.close)

        saveChangesButton = QPushButton('Save Changes')
        footerLayout.addWidget(saveChangesButton)
        saveChangesButton.clicked.connect(self.close)

        pageLayout.addWidget(footerButtons)

    # This function shows the basic info tab page
    def basic_info_TabView(self):
        self.basicInfoPage = QWidget()
        basicInfoPageLayout = QGridLayout(self.basicInfoPage)

        self.fullName = QLineEdit()
        self.fullName.setPlaceholderText("Full Name")
        basicInfoPageLayout.addWidget(self.fullName, 0, 0)

        self.prisonRoleID = QLineEdit()
        self.prisonRoleID.setPlaceholderText("Prison Role ID")
        basicInfoPageLayout.addWidget(self.prisonRoleID, 1, 0)

        self.homeAddress = QLineEdit()
        self.homeAddress.setPlaceholderText("Home Address")
        basicInfoPageLayout.addWidget(self.homeAddress, 2, 0)

        self.prisonerGender = QComboBox()
        self.prisonerGender.addItem("Male")
        self.prisonerGender.addItem("Female")
        basicInfoPageLayout.addWidget(self.prisonerGender, 3, 0)

        self.releaseDate = QLineEdit()
        self.releaseDate.setPlaceholderText("Release Date")
        basicInfoPageLayout.addWidget(self.releaseDate, 4, 0)

        self.expectedEndOfLicence = QLineEdit()
        self.expectedEndOfLicence.setPlaceholderText("Expected End Of Licence")
        basicInfoPageLayout.addWidget(self.expectedEndOfLicence, 0, 1)

        self.currentPrison = QLineEdit()
        self.currentPrison.setPlaceholderText("Current Prison Location")
        basicInfoPageLayout.addWidget(self.currentPrison, 1, 1)

        self.additionalNotes = QLineEdit()
        self.additionalNotes.setPlaceholderText("Additional Notes")
        basicInfoPageLayout.addWidget(self.additionalNotes, 2, 1)

        self.prisonerCategory = QComboBox()
        self.prisonerCategory.addItem("Prisoner")
        basicInfoPageLayout.addWidget(self.prisonerCategory, 3, 1)

        self.prisonerPhoto = QLineEdit()
        self.prisonerPhoto.setPlaceholderText("Prisoner Photo")
        basicInfoPageLayout.addWidget(self.prisonerPhoto, 4, 1)

    # This function shows the requirements tab page
    def requirements_TabView(self):
        self.requirementsPage = QWidget()
        requirementsPageLayout = QVBoxLayout(self.requirementsPage)

        restrictionsSection = QWidget()
        restrictionsLayout = QVBoxLayout(restrictionsSection)
        restrictionsSectionLabel = QLabel("Restrictions")
        restrictionsLayout.addWidget(restrictionsSectionLabel)

        restrictionCheckboxes = QWidget()
        restrictionCheckboxesLayout = QGridLayout(restrictionCheckboxes)
        self.drugSearch = QCheckBox('Requires drug searches')

        self.priorRHUExperience = QCheckBox('Has prior RHU experience')

        self.offendingTriggers = QComboBox()
        self.offendingTriggers.addItem("No offending triggers")
        self.offendingTriggers.addItem("Gambling")
        self.offendingTriggers.addItem("Alcohol")
        self.offendingTriggers.addItem("Others")

        self.periodOfLicence = QLineEdit()
        self.periodOfLicence.setPlaceholderText("Period of licence, 01/12/23")

        self.ageGroup = QComboBox()
        self.ageGroup.addItem("Select age group..")
        self.ageGroup.addItem("Young Adults (18 years old and below")
        self.ageGroup.addItem("Adult (18 years old and above)")
        self.ageGroup.addItem("Old adults (60 years old and above)")

        self.gender = QComboBox()
        self.gender.addItem("Select RHU gender suitability..")
        self.gender.addItem("Male only")
        self.gender.addItem("Female only")
        self.gender.addItem("Mixed")

        # Since I utilised a grid layout, I should provide the grid coordinates so buttons could be placed properly
        restrictionCheckboxesLayout.addWidget(self.drugSearch, 0, 0)
        restrictionCheckboxesLayout.addWidget(self.priorRHUExperience, 0, 1)
        restrictionCheckboxesLayout.addWidget(self.offendingTriggers, 1, 0)
        restrictionCheckboxesLayout.addWidget(self.periodOfLicence, 1, 1)
        restrictionCheckboxesLayout.addWidget(self.ageGroup, 2, 0)
        restrictionCheckboxesLayout.addWidget(self.gender, 2, 1)

        restrictionsLayout.addWidget(restrictionCheckboxes)

        self.curfew = QComboBox()
        self.curfew.addItem("No curfew required")
        self.curfew.addItem("Requires nighttime curfew")
        self.curfew.addItem("Requires weekend curfew")

        restrictionsLayout.addWidget(self.curfew)

        requirementsPageLayout.addWidget(restrictionsSection)

        exclusionZonesSection = QWidget()
        exclusionZonesSectionLayout = QVBoxLayout(exclusionZonesSection)
        exclusionZonesWidgetLabel = QLabel("Exclusion Zones")
        exclusionZonesSectionLayout.addWidget(exclusionZonesWidgetLabel)
        exclusionZonesCheckboxes = QWidget()
        exclusionZonesCheckboxesLayout = QHBoxLayout(exclusionZonesCheckboxes)
        self.victimExclusionZones = QCheckBox('Exclusion zones around victims')
        self.schoolExclusionZones = QCheckBox('Exclusion zones around schools')
        self.locationofExclusionZones = QLineEdit()
        self.locationofExclusionZones.setPlaceholderText('Provide the location of the exclusion zones')
        exclusionZonesCheckboxesLayout.addWidget(self.victimExclusionZones)
        exclusionZonesCheckboxesLayout.addWidget(self.schoolExclusionZones)
        exclusionZonesCheckboxesLayout.addWidget(self.locationofExclusionZones)
        exclusionZonesSectionLayout.addWidget(exclusionZonesCheckboxes)

        requirementsPageLayout.addWidget(exclusionZonesSection)

        healthRequirementsSection = QWidget()
        healthRequirementsLayout = QVBoxLayout(healthRequirementsSection)
        healthRequirementsLabel = QLabel("Health Requirements")
        healthRequirementsLayout.addWidget(healthRequirementsLabel)

        mentalHealthConditions = QComboBox()
        mentalHealthConditions.addItem("No mental health conditions")
        mentalHealthConditions.addItem("PTSD")
        mentalHealthConditions.addItem("Depression")
        mentalHealthConditions.addItem("Schizophrenic")
        mentalHealthConditions.addItem("Others")
        healthRequirementsLayout.addWidget(mentalHealthConditions)

        disabilityComboBox = QComboBox()
        disabilityComboBox.addItem("No disability")
        disabilityComboBox.addItem("Autism")
        disabilityComboBox.addItem("ADHD")
        disabilityComboBox.addItem("Dyslexia")
        disabilityComboBox.addItem("Blindness")
        disabilityComboBox.addItem("Others")

        accessibilityNote = QLineEdit()
        accessibilityNote.setPlaceholderText("Provide the accessibility notes here")
        healthRequirementsLayout.addWidget(disabilityComboBox)
        healthRequirementsLayout.addWidget(accessibilityNote)

        healthRequirementsLayout.addWidget(disabilityComboBox)
        healthRequirementsLayout.addWidget(accessibilityNote)

        requirementsPageLayout.addWidget(healthRequirementsSection)

        accessToServices = QWidget()
        accessToServicesLayout = QVBoxLayout(accessToServices)
        accessToServicesLabel = QLabel("Access to Services")
        accessToServicesLayout.addWidget(accessToServicesLabel)

        accessToServicesCheckboxes = QWidget()
        accessToServicesCheckboxesLayout = QGridLayout(accessToServicesCheckboxes)
        medicalServices = QCheckBox('Medical Services (Hospitals, clinics, etc.)')
        transportLinks = QCheckBox('Transport Links (Bus routes, train railways etc.)')
        religiousServices = QCheckBox('Religious Services (Church, mosque etc.)')
        employmentServices = QCheckBox('Employment Services (Job centers, approved workplace etc.)')
        familyConnections = QLineEdit()
        familyConnections.setPlaceholderText('Provide the Family or Relative Connections here (Father, Wife etc.)')

        accessToServicesCheckboxesLayout.addWidget(medicalServices, 0, 0)
        accessToServicesCheckboxesLayout.addWidget(transportLinks, 0, 1)
        accessToServicesCheckboxesLayout.addWidget(religiousServices, 1, 0)
        accessToServicesCheckboxesLayout.addWidget(employmentServices, 1, 1)
        accessToServicesCheckboxesLayout.addWidget(familyConnections, 2, 0)

        accessToServicesLayout.addWidget(accessToServicesCheckboxes)

        requirementsPageLayout.addWidget(accessToServices)

        futureExpansionSection = QWidget()
        futureExpansionLayout = QVBoxLayout(futureExpansionSection)
        futureExpansionLabel = QLabel("Additional Requirements - Student Suggested")
        futureExpansionLayout.addWidget(futureExpansionLabel)

        futureExpansion2Label = QLabel("Future Expansion 2")
        self.futureExpansion2 = QLineEdit()
        self.futureExpansion2.setPlaceholderText("Provide a placeholder text here..")
        futureExpansionLayout.addWidget(futureExpansion2Label)
        futureExpansionLayout.addWidget(self.futureExpansion2)

        futureExpansion3Label = QLabel("Future Expansion 3")
        self.futureExpansion3 = QLineEdit()
        self.futureExpansion3.setPlaceholderText("Provide a placeholder text here..")
        futureExpansionLayout.addWidget(futureExpansion3Label)
        futureExpansionLayout.addWidget(self.futureExpansion3)

        futureExpansion1Label = QLabel("Future Expansion 3")
        self.futureExpansion1 = QLineEdit()
        self.futureExpansion1.setPlaceholderText("Provide a placeholder text here..")
        futureExpansionLayout.addWidget(futureExpansion1Label)
        futureExpansionLayout.addWidget(self.futureExpansion1)

        requirementsPageLayout.addWidget(futureExpansionSection)

        additionalRequirementsSection = QWidget()
        additionalRequirementsLayout = QVBoxLayout(additionalRequirementsSection)
        additionalRequirementsLabel = QLabel("Additional Requirements - Student Suggested")
        additionalRequirementsLayout.addWidget(additionalRequirementsLabel)

        therapyServiceLabel = QLabel("Therapy Service")
        self.therapyService = QLineEdit()
        self.therapyService.setPlaceholderText("Explain what therapy services are needed here")
        additionalRequirementsLayout.addWidget(therapyServiceLabel)
        additionalRequirementsLayout.addWidget(self.therapyService)

        financialSupportLabel = QLabel("Financial Support")
        self.financialSupport = QLineEdit()
        self.financialSupport.setPlaceholderText("What kind of financial support is needed?")
        additionalRequirementsLayout.addWidget(financialSupportLabel)
        additionalRequirementsLayout.addWidget(self.financialSupport)

        requirementsPageLayout.addWidget(additionalRequirementsSection)

    # This function shows the additional notes tab page
    def add_notes_TabView(self):
        self.addNotesPage = QWidget()
        addNotesPageLayout = QVBoxLayout(self.addNotesPage)

        addNotesLabel = QLabel("Additional Notes for Prisoner")
        addNotesPageLayout.addWidget(addNotesLabel)

        addNotesField = QLineEdit()
        addNotesField.setPlaceholderText("Enter additional notes here (prisoner's special requirements, etc.)")
        addNotesPageLayout.addWidget(addNotesField)

# This class handles the main homepage window of the app
class HomepageWindow(QMainWindow):
    def __init__(self):
        super().__init__()  # Inheriting QMainWindow attributes
        self.setWindowTitle("RHU App Homepage")
        self.resize(800, 600)   # Resizing window to appropriate size

        overviewContainer = QWidget(self)
        self.setCentralWidget(overviewContainer)
        overviewLayout = QVBoxLayout(overviewContainer)

        # This is a navigation tab bar that houses buttons to change between different page tabs
        navBar = QWidget()
        navBarLayout = QHBoxLayout(navBar)

        overviewTab = QPushButton('Overview')
        navBarLayout.addWidget(overviewTab)
        overviewTab.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(0))

        RHUTab = QPushButton('RHUs')
        navBarLayout.addWidget(RHUTab)
        RHUTab.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(1))   # lambda is used to simplify code

        overviewLayout.addWidget(navBar)

        self.stackedWidget = QStackedWidget()

        # Function Calling Overview tab container
        self.overview_TabView()

        # Function calling RHU Tab Container
        self.RHU_TabView()

        self.stackedWidget.addWidget(self.mainContainer)
        self.stackedWidget.addWidget(self.RHUContainer)

        overviewLayout.addWidget(self.stackedWidget)

    # This function directs the button clicked action to AddNewLicencee function to open its dialog window
    def open_registration_window(self):
        dialog = AddLicenceeWindow()
        dialog.setWindowTitle("Add A New Licencee")
        dialog.exec()

    # This function show the overview tab page
    def overview_TabView(self):
        # Main Container for Overview
        self.mainContainer = QWidget()
        homepageLayout = QVBoxLayout(self.mainContainer)

        # Header Bar with its search, sort and add new licencee button functionality
        headerBar = QWidget()
        headerbarLayout = QHBoxLayout(headerBar)

        self.searchBar = QLineEdit()
        self.searchBar.setPlaceholderText("Search by name or Prisoner ID")
        headerbarLayout.addWidget(self.searchBar)
        self.searchBar.text()

        filterSort = QComboBox()
        filterSort.addItems(['Sort by Date', 'Sort by Name', 'Sort by Prisoner ID'])
        headerbarLayout.addWidget(filterSort)

        searchButton = QPushButton("Search")
        headerbarLayout.addWidget(searchButton)

        addNewLicencee = QPushButton("+ Add A New Licencee")
        addNewLicencee.clicked.connect(self.open_registration_window)
        headerbarLayout.addWidget(addNewLicencee)

        homepageLayout.addWidget(headerBar)

        # Here are the 3 types of licencee columns section
        licenceeSection = QWidget()
        licenceeLayout = QHBoxLayout(licenceeSection)

        licenceeLabelSection = QWidget()
        licenceeLabelLayout = QHBoxLayout(licenceeLabelSection)

        # Each section is labelled with their respective labels to differentiate
        pendingLicenceeLabel = QLabel("Pending Licence")
        licenceeLabelLayout.addWidget(pendingLicenceeLabel)

        # Creation of list of licencee using the provided self.data
        self.pendingLicencee = QListView()
        self.data = [
            {'name': 'Dustin'},
            {'name': 'Johnathan'},
            {'name': 'Hop'},
            {'name': 'Anderson'},
            {'name': 'Jim'},
            {'name': 'Robin'},
            {'name': 'Steve'},
            {'name': 'Asher'},
            {'name': 'Barbara'},
            {'name': 'Will'},
            {'name': 'Mike'},
            {'name': 'Dustin'},
            {'name': 'Johnathan'},
            {'name': 'Hop'},
            {'name': 'Keema'},
            {'name': 'Powell'},
            {'name': 'Howard'},
            {'name': 'Christabel'},
            {'name': 'Joseph'},
            {'name': 'Muji'},
            {'name': 'Lee'},
        ]

        self.overviewModel = CustomListModel(self.data)

        self.pendingLicencee.setModel(self.overviewModel)

        self.pendingLicencee.setItemDelegate(CustomItemDelegate())
        licenceeLayout.addWidget(self.pendingLicencee)

        allocatedHouseLabel = QLabel("Allocated Housing")
        licenceeLabelLayout.addWidget(allocatedHouseLabel)

        self.allocatedHouse = QListView()
        self.data = [
            {'name': 'Dustin'},
            {'name': 'Johnathan'},
            {'name': 'Hop'},
            {'name': 'Anderson'},
            {'name': 'Jim'},
            {'name': 'Robin'},
            {'name': 'Steve'},
            {'name': 'Asher'},
            {'name': 'Barbara'},
            {'name': 'Will'},
            {'name': 'Mike'},
            {'name': 'Dustin'},
            {'name': 'Johnathan'},
            {'name': 'Hop'},
            {'name': 'Keema'},
            {'name': 'Powell'},
            {'name': 'Howard'},
            {'name': 'Christabel'},
            {'name': 'Joseph'},
            {'name': 'Muji'},
            {'name': 'Lee'},
        ]

        self.overviewModel = CustomListModel(self.data)

        self.allocatedHouse.setModel(self.overviewModel)

        self.allocatedHouse.setItemDelegate(CustomItemDelegate())
        licenceeLayout.addWidget(self.allocatedHouse)

        exitedSystemLabel = QLabel("Exited System")
        licenceeLabelLayout.addWidget(exitedSystemLabel)

        self.exitedSystem = QListView()
        self.data = [
            {'name': 'Dustin'},
            {'name': 'Johnathan'},
            {'name': 'Hop'},
            {'name': 'Anderson'},
            {'name': 'Jim'},
            {'name': 'Robin'},
            {'name': 'Steve'},
            {'name': 'Asher'},
            {'name': 'Barbara'},
            {'name': 'Will'},
            {'name': 'Mike'},
            {'name': 'Dustin'},
            {'name': 'Johnathan'},
            {'name': 'Hop'},
            {'name': 'Keema'},
            {'name': 'Powell'},
            {'name': 'Howard'},
            {'name': 'Christabel'},
            {'name': 'Joseph'},
            {'name': 'Muji'},
            {'name': 'Lee'},
        ]

        self.overviewModel = CustomListModel(self.data)

        self.exitedSystem.setModel(self.overviewModel)

        self.exitedSystem.setItemDelegate(CustomItemDelegate())
        licenceeLayout.addWidget(self.exitedSystem)

        homepageLayout.addWidget(licenceeLabelSection)
        homepageLayout.addWidget(licenceeSection)

    # This function directs the button clicked action to AddRHUWindow function to open its dialog window
    def open_RHU_regisration_window(self):
        dialog = AddRHUWindow()
        dialog.setWindowTitle("Add A New RHU")
        dialog.exec()

    # This function show the RHU tab page
    def RHU_TabView(self):
        self.RHUContainer = QWidget()
        RHUContainerLayout = QVBoxLayout(self.RHUContainer)

        headerBar = QWidget()
        headerBarLayout = QHBoxLayout(headerBar)

        self.searchBar = QLineEdit()
        self.searchBar.setPlaceholderText("Search housing name")
        headerbarLayout.addWidget(self.searchBar)
        self.searchBar.text()

        # Add RHU button goes here!
        addRHUButton = QPushButton("Add A New RHU")
        headerBarLayout.addWidget(addRHUButton)
        addRHUButton.clicked.connect(self.open_RHU_regisration_window)

        RHUContainerLayout.addWidget(headerBar)

        RHUSection = QWidget()
        RHUSectionLayout = QVBoxLayout(RHUSection)

        # Creating a list view to show list of available housing units
        RHUListViewLabel = QLabel("RHU List")
        RHUSectionLayout.addWidget(RHUListViewLabel)

        # Data for the housing unit list
        self.RHUListView = QListView()
        self.data2 = [
            {'name': 'Durham County Hostel'},
            {'name': 'Crook Hostel'},
            {'name': 'Villa Grandview'},
            {'name': 'Famosa Motel'},
            {'name': 'Flakes Housing'},
            {'name': 'Marisa Viewland'},
            {'name': 'Hawkins High'},
            {'name': 'Northumberland County Manor'},
            {'name': 'Heinz Hotel'},
            {'name': 'Karl Shared Housing'},
            {'name': 'Zeiss Shared Housing'},
            {'name': 'Mount Hostel'},
            {'name': 'Elton Hostel'},
        ]

        self.RHUmodel = CustomListModel(self.data2)

        self.RHUListView.setModel(self.RHUmodel)

        self.RHUListView.setItemDelegate(CustomItemDelegate())
        RHUSectionLayout.addWidget(self.RHUListView)

        RHUContainerLayout.addWidget(RHUSection)

# This class handles login window where user can enter their password to access the app's homepage
class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__() # Inheriting attributes from the superclass QMainWindow
        self.setWindowTitle("RHU App Login") # Setting the window title to differentiate between windows
        self.resize(200, 300) # Resizing the window to appropriate size

        mainContainer = QWidget(self)
        self.setCentralWidget(mainContainer) # Setting mainContainer as central widget

        loginLayout = QVBoxLayout(mainContainer)

        label = QLabel('On-Licence Housing Allocation System')
        self.loginPassword = QLineEdit()
        self.loginPassword.setPlaceholderText("Password is AOdurham2026")   # This gives an idea of what the set password is to user
        loginButton =  QPushButton('Login')
        loginButton.clicked.connect(self.open_homepage) # Event driven button which connects to the password validation function in this class

        # Adding all the widgets into main widget layout
        loginLayout.addWidget(label)
        loginLayout.addWidget(self.loginPassword)
        loginLayout.addWidget(loginButton)

    # This function does the password validation work
    def open_homepage(self):
        password = self.loginPassword.text()
        if password == "AOdurham2026":  # Checks user input in password box whether it's the same as set password
            self.homepage = HomepageWindow()
            self.homepage.show()
            self.close()    # If yes, homepage window will open and login window is closed
        else:
            QMessageBox.warning(self, "Error", "Wrong Password")    # If not, a message box will appear saying user entered wrong password

# Main section of the code where first window of the app is called for execution
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    app.exec()
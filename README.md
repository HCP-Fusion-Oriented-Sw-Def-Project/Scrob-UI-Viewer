# Scrob-UI-Viewer

######
An tool to show and record GUI changes for Android apps.

Similiar to `uiautomatorviewer`, it could be used to locate GUI elements and get related GUI information in a screen.

## Requirement

######
* Python 3.7.6
* All the other requirements are listed in the requirements.txt.

## Run Scrob UI Viewer
1. `git clone` the project in a directory, e.g., 'work_dir'.
2. Find the file  `work_dir/dist/test/Scrob UI Viewer.exe` and double click it.

## How to Use
* Basic 
  * **New**: Create a project by a pair of GUI data, which includes images and xml files.
    * When the project is successfully created, all the leaf elements are displayed in the Visible pane and the recommended element matches are displayed in the Matched pane.
    * We could move the elements in the panes as we want.
  * **Open**: Open an exist project.
  * **Restore**: Restore the project as it was just opened.
  * **Save**: Save the Project/Save changes.
  * **Save as**: Save the Project in another directory.
  * **Clear**: Clear the all information in the project. If mis-operating, try to restore the project.
  * **Click**: When click an element in the image, we could get its information at the top right.
* Move
* Search
* Pane

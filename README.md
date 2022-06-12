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
    * When the project is successfully created, all the leaf elements are displayed in the visible pane and the recommended element matches are displayed in the matched pane.
    * We could move the elements in the panes as we want.
  * **Open**: Open an exist project.
  * **Restore**: Restore the project as it was just opened.
  * **Save**: Save the Project/Save changes.
  * **Save as**: Save the Project in another directory.
  * **Clear**: Clear the all information in the project. If mis-operating, try to restore the project.
  * **Click**: When clicking an element in the image, we could get its information at the top right.
* Move
  1. Choose app version.
  2. Choose element type, e.g., leaf/branch.
  3. Move the element to the panes (visible/removed/changed/added).
* Search
  * Search elements in the screen by their attributes (no/bounds/xpath).
* Panes
  * Common Operation
     * `delete`: Delete the element in this pane.
     * `locate`: Locate the element in the screen.
     * `refresh`: Update all the panes.
  * Visible 
    * `update invisible list`: The elements deleted in this pane will be added to invisible pane.
    * `mark list elements`: Mark the element as elements in slide list.
    * `add to removed list`: Add the element to removed pane.
    * `add to changed list`: Add the element to changed pane.
    * `add to added list`: Add the element to added pane.
  * Removed
  * Changed
    * Record the attributes state: 0/1, e.g., 0->no changes, 1->changed.
    * `Save`: Save the attributes state once it has changed.
  * Added
  * Invisible
  * Matched
    * `add to changed list`: Add the element to removed pane.
    * `add locate elements here`: Assure that two elements are selected respectively in the base and updated screens, add them in matched pane.
    * `update removed and added list`: If the elements in matched pane are considered appropriate, the rest elements in base screen will be added to removed pane, the rest elements in updated screen will be added to added pane.
  * `Draw all`: Draw all the elements in choosed pane on the corresponding screen.
* Element Detail
  * index
  * class
  * id
  * text
  * desc
  * width/height
  * location
  * No: The element number in the screen according to the order of depth-first traversal.
  * layer: The level at the GUI hierarchical tree.
  * type: leaf/branch
  * clickable

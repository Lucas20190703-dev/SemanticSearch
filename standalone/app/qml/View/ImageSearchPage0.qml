import QtCore
import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import Qt.labs.platform as L

import KQuick.Controls 1.0
import KQuick.Core 1.0

BasePage {
    id: _root

    property bool previewEnabled: true

    title: qsTr("Search")
    
    padding: 0

    Component.onCompleted: _hSplitView.restoreState(_settings.splitView)
    Component.onDestruction: _settings.splitView = _hSplitView.saveState()

    Settings {
        id: _settings
        property alias rootDir: _directoryPath.text
        property alias previewEnabled: _root.previewEnabled
        property var splitView
    }

    Item {
        id: _dirPane
        width: parent.width
        height: 32

        Row {
            x: 12
            height: parent.height
            
            KButton {
                anchors.verticalCenter: parent.verticalCenter
                text: qsTr("Root Directory")
                textColor: hovered? Colors.accent.highlight : Colors.accent.primary
                icon {
                    source: "qrc:/icons/folder.svg"
                    width: 16
                    height: 16
                    color: hovered? Colors.accent.highlight : Colors.accent.primary
                }
                flat: true
                onClicked: _folderDialog.open()
            }
            
            KLabel {
                anchors.verticalCenter: parent.verticalCenter
                text: ":"
                color: Colors.accent.primary
            }

            KLabel {
                id: _directoryPath
                anchors.verticalCenter: parent.verticalCenter
                leftPadding: 10
                color: Colors.accent.primary
            }
        }

        Item {
            width: 42
            height: parent.height
            anchors.right: parent.right

            Rectangle {
                width: 18
                height: 16
                color: "transparent"
                border {
                    width: 2
                    color: Colors.accent.primary
                }
                radius: 2

                Rectangle {
                    anchors.centerIn: parent
                    width: 2
                    height: parent.height
                    color: Colors.accent.primary
                    visible: !previewEnabled
                }
            }
            TapHandler {
                onTapped: {
                    previewEnabled = !previewEnabled;
                }
            }
        }
    }

    KSeparator {
        anchors {
            top: _dirPane.bottom
        }
        width: parent.width
    }

    SplitView {
        id: _hSplitView
        anchors.fill: parent
        anchors.topMargin: 34
        
        orientation: Qt.Horizontal

        handle: KSplitHandle { 
            Rectangle {
                anchors.centerIn: parent
                width: 2
                height: parent.height
                color: Colors.border.primary
                visible: _root.previewEnabled
            }
        }

        ImageListView {
            id: _imageListPane
            SplitView.fillWidth: true
            SplitView.fillHeight: true
            rootDir: _directoryPath.text
        }

        PreviewPane {
            id: _previewPane
            SplitView.preferredWidth: _root.previewEnabled? 400 : 0
            SplitView.fillHeight: true
            SplitView.minimumWidth: _root.previewEnabled? 250 : 0
            SplitView.maximumWidth: parent.width / 2
            
            selectedItem: _imageListPane.selectedItem
        }
    }
    
    L.FolderDialog {
		id: _folderDialog
        folder: _settings.rootDir || "file:///" + pictureLocation
		onAccepted: {
			let dir = _folderDialog.folder.toString();
			if (dir.startsWith("file:///")) {
				dir = dir.substring(8);
			}
			_directoryPath.text = dir;
		}
	}

    
}
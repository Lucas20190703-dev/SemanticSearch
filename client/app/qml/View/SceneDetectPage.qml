import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

import KQuick.Controls
import KQuick.Core

BasePage {
    title: qsTr("Home")

    SplitView {
        anchors.fill: parent
        handle: KSplitHandle {
            implicitWidth: 11
            Rectangle {
                width: 1
                height: parent.height
                anchors.centerIn: parent
                color: Colors.control.border.primary
            }
        }

        DirectoryTreeView {
            id: _folderTreeview
            SplitView.preferredWidth: 240
            SplitView.fillHeight: true
        }

        DirectoryContentView {
            id: _contentView
            SplitView.fillWidth: true
            SplitView.fillHeight: true
            folder: _folderTreeview.selected
        }

        PreviewPane {
            id: _previewPane
            SplitView.preferredWidth: 300
            SplitView.fillHeight: true
            selectedItem: _contentView.selected
        }
    }
}
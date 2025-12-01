import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

import KQuick.Controls
import KQuick.Core

ColumnLayout {
    property alias folder: _contentView.folder

    SearchPanel {
        id: _searchPanel
        Layout.fillWidth: true
    }

    SplitView {
        Layout.fillWidth: true
        Layout.fillHeight: true

        handle: KSplitHandle {
            implicitWidth: 11
            Rectangle {
                width: 1
                height: parent.height
                anchors.centerIn: parent
                color: Colors.control.border.primary
            }
        }

        DirectoryContentView {
            id: _contentView
            SplitView.fillWidth: true
            SplitView.fillHeight: true
            filterPattern: _searchPanel.nameFilter
            startDate: _searchPanel.startDateFilter
            endDate: _searchPanel.endDateFilter
            dateFilterEnabled: _searchPanel.dateFilterEnabled
        }

        PreviewPane {
            id: _previewPane
            SplitView.preferredWidth: 340
            SplitView.fillHeight: true
            selectedItem: _contentView.selected
        }
    }

}
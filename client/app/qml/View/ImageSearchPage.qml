import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

import KQuick.Controls

BasePage {
    title: qsTr("Search")

    ColumnLayout {
        anchors.fill: parent
        SearchPanel {
            id: _searchPanel
            Layout.fillWidth: true
            
            onNameFilterChanged: {
                console.log("Name filter changed:");
                //searchEngine.fileModel.setSearchText(nameFilter);
            }

            onCaptionFilterChanged: {
                //searchEngine.fileModel.setSearchCaption(captionFilter);
            }

            onSimilarityChanged: {
                //searchEngine.fileModel.setSearchCaptionThreshold(similarity);
            }

            onStartDateFilterChanged: {
                //searchEngine.fileModel.setSearchDate(startDateFilter, endDateFilter);
            }

            onEndDateFilterChanged: {
                //searchEngine.fileModel.setSearchDate(startDateFilter, endDateFilter);
            }
        }
        
        KSeparator {
            Layout.fillWidth: true
        }

        Item {
            Layout.fillWidth: true
            Layout.fillHeight: true
        }
    }
}
import QtQuick
import QtQuick.Layouts
import QtQuick.Controls

import KQuick.Controls
import KQuick.Core
import Utils 1.0

Item {
    id: _root
    property var selectedItem: null
    
    onSelectedItemChanged: {
        _sceneModel.clear();
        if (selectedItem) {
            // reset model
            if (selectedItem.fileType === "video") {
                //sceneDetector.generateKeyframes(Constants.removePrefix(selectedItem.filePath));
            }
        }
    }

    Connections {
        target: sceneDetector

        function onFinished(res) {
            const result = JSON.parse(res);
            if (result.file === Constants.removePrefix(selectedItem.filePath)) {
                for (let s of result.scenes) {
                    _sceneModel.append(s);
                }
            }
        }
    }

    ColumnLayout {
        anchors.fill: parent
        anchors.margins: 9

        visible: selectedItem

        Item {
            Layout.fillWidth: true
            Layout.preferredHeight: _metaGrid.implicitHeight

            GridLayout {
                id: _metaGrid
                width: parent.width

                columnSpacing: 9
                rowSpacing: 9
                
                columns: 2

                KLabel {
                    text: qsTr("Name:")
                }

                KLabel {
                    text: _root.selectedItem? _root.selectedItem.fileName : ""
                }

                KLabel {
                    text: qsTr("Path:")
                }

                KLabel {
                    Layout.fillWidth: true
                    text: _root.selectedItem? Constants.removePrefix(Constants.parentPath(_root.selectedItem.filePath)) : ""
                    elide: Text.ElideLeft
                    
                }

                
                KLabel {
                    text: qsTr("Type:")
                }

                KLabel {
                    text: _root.selectedItem? _root.selectedItem.fileType : "Unknown"
                    font.capitalization: Font.Capitalize
                }

                KLabel {
                    text: qsTr("Size:")
                }

                KLabel {
                    Layout.fillWidth: true
                    text: _root.selectedItem? Constants.formatFileSize(_root.selectedItem.fileSize) : ""
                    elide: Text.ElideLeft
                }

                KLabel {
                    text: qsTr("Keywords:")
                }

                KLabel {
                    Layout.fillWidth: true
                    text: _root.selectedItem && _root.selectedItem.keywords? `[ ${_root.selectedItem.keywords.join(', ')} ]` : ""
                    wrapMode: Text.Wrap
                }

                KLabel {
                    text: qsTr("Modified:")
                }

                KLabel {
                    Layout.fillWidth: true
                    text: _root.selectedItem && _root.selectedItem.modified? Constants.timestamp2Date(_root.selectedItem.modified) : ""
                    elide: Text.ElideLeft
                }
            }
        }

        KSeparator { Layout.fillWidth: true; verticalPadding: 12 }

        Item {
            Layout.fillWidth: true
            Layout.fillHeight: true
            Row {
                spacing: 6
                KLabel {
                    text: qsTr("Scenes:")
                }

                KLabel {
                    text: _sceneModel.count
                }
            }
            ScrollView {
                anchors.fill: parent
                anchors.topMargin: 24

                clip: true
                contentWidth: width
                contentHeight: grid.height

                Grid {
                    id: grid
                    property int cellWidth: 160 + 12
                    property int cellHeight: 90

                    width: parent.width

                    columns: Math.max(1, Math.floor(width / cellWidth))
                    columnSpacing: (columns < 2)? 10 : (width - columns * grid.cellWidth) / (columns - 1)
                    rowSpacing: 10

                    Repeater {
                        id: _itemRepeater
                        model: _sceneModel

                        delegate: Column {
                            id: _itemDelegate
                            width: grid.cellWidth
                            spacing: 4

                            MediaItem {
                                source: thumbnail
                                sourceType: "image"
                            }
                            Item {
                                anchors.horizontalCenter: parent.horizontalCenter
                                width: grid.cellWidth
                                height: grid.cellHeight
                                
                                Image {
                                    anchors.fill: parent
                                    anchors.margins: 1
                                    fillMode: Image.PreserveAspectFit
                                    sourceSize: Qt.size(width, height)
                                    source: thumbnail   
                                }
                                Rectangle {
                                    anchors.fill: parent
                                    border {
                                        width: _itemDelegate.isSelected? 2 : 1
                                        color: _itemDelegate.isSelected? Colors.control.border.highlight : Colors.control.border.primary
                                    }
                                    color: "transparent"
                                }

                                TapHandler {
                                    onDoubleTapped: {
                                        openPreviewImage(thumbnail, "image");
                                    }
                                }
                            }

                            RowLayout {
                                width: parent.width - 12
                                anchors.horizontalCenter: parent.horizontalCenter
                                KText { 
                                    Layout.fillWidth: true
                                    text: start_time
                                    font.pointSize: 8 
                                    elide: Text.ElideRight
                                }

                                KText { 
                                    Layout.fillWidth: true
                                    horizontalAlignment: Text.AlignRight
                                    text: end_time
                                    font.pointSize: 8 
                                    elide: Text.ElideRight
                                }
                            }
                        }
                    }
                }
            }
        }
    }

    ListModel {
        id: _sceneModel
    }
}
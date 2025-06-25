import QtQuick
import QtQuick.Layouts

import KQuick.Core
import KQuick.Controls

Item {
    id: _root
    property alias model: _itemRepeater.model

    property int cellWidth: 160
    property int cellHeight: 90

    property var selected

    Grid {
        id: grid
        property int cellWidth: 160 + 12
        property int cellHeight: 90

        anchors {
            fill: parent
            leftMargin: 16
            rightMargin: 16
            topMargin: 6
            bottomMargin: 6
        }

        columns: Math.max(1, Math.floor(width / cellWidth))
        columnSpacing: (columns < 2)? 6 : (width - columns * grid.cellWidth) / (columns - 1)
        rowSpacing: 10

        Repeater {
            id: _itemRepeater

            delegate: Column {
                id: _itemDelegate
                width: grid.cellWidth
                spacing: 4

                readonly property bool isSelected: _root.selected && _root.selected.path === path

                Item {
                    anchors.horizontalCenter: parent.horizontalCenter
                    width: grid.cellWidth - 12
                    height: grid.cellHeight
                    
                    Image {
                        anchors.fill: parent
                        anchors.margins: 1
                        fillMode: Image.PreserveAspectFit
                        sourceSize: Qt.size(width, height)
                        source: path
                    }

                    KIcon {
                        anchors.centerIn: parent
                        width: 32
                        height: 32
                        visible: type === "video"
                        icon {
                            width: 32
                            height: 32
                            source: "qrc:/icons/video.png"
                            color: Colors.accent.highlight
                        }
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
                            openPreviewImage(path, type);
                        }

                        onTapped: {
                            _root.selected = {
                                name,
                                path,
                                type
                            }
                        }
                    }
                }

                KText { 
                    anchors.horizontalCenter: parent.horizontalCenter
                    width: Math.min((parent.width - 12) * 0.8, implicitWidth)
                    text: name
                    font.pointSize: 8 
                    elide: Text.ElideRight
                }
            }
        }
    }
}
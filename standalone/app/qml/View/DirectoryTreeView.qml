import QtQuick
import QtQuick.Controls
import KQuick.Controls
import KQuick.Core

Item {
    id: _root

    property var selected

    Component.onCompleted: {
        _treeView.expandRecursively()
    }
    
    TreeView {
        id: _treeView
        anchors.fill: parent
        model: directoryModel
        
        selectionModel: ItemSelectionModel {}

        rowHeightProvider: function(row) { return 24 }
        clip: true

        flickableDirection: Flickable.AutoFlickIfNeeded
        
        delegate: Item {
            id: _delegate
            readonly property real indentation: 16
            readonly property real padding: 10

            // Assigned to by TreeView:
            required property TreeView treeView
            required property bool isTreeNode
            required property bool expanded
            required property bool hasChildren
            required property int depth
            required property int row
            required property int column
            required property bool current

            required property string display
            required property string path

            implicitWidth: Math.max(padding + label.x + label.implicitWidth + padding, _treeView.width)
            implicitHeight: label.implicitHeight * 1.5

            // Rotate indicator when expanded by the user
            // (requires TreeView to have a selectionModel)
            // property Animation indicatorAnimation: NumberAnimation {
            //     target: indicator
            //     property: "rotation"
            //     from: expanded ? 0 : 90
            //     to: expanded ? 90 : 0
            //     duration: 100
            //     easing.type: Easing.OutQuart
            // }
            // TableView.onPooled: indicatorAnimation.complete()
            // TableView.onReused: if (current) indicatorAnimation.start()
            // onExpandedChanged: indicator.rotation = expanded ? 90 : 0

            Rectangle {
                id: background
                anchors.fill: parent
                color: row === treeView.currentRow ? Colors.control.background.highlight : "transparent"
                opacity: 0.8 //(treeView.alternatingRows && row % 2 !== 0) ? 0.3 : 0.1
            }

            
            TapHandler {
                onTapped: {
                    if (_root.selected == path) {
                        return;
                    }
                    _root.selected = path;
                }    
            }

            KIcon {
                id: indicator
                anchors.verticalCenter: parent.verticalCenter
                height: parent.height
                width: height 
                x: _delegate.padding + (depth * indentation)

                icon {
                    width: 12
                    height: 12
                    color: Colors.accent.primary
                    source: isTreeNode && hasChildren? (expanded? "qrc:/icons/open-folder.png" : "qrc:/icons/folder.png") : "qrc:/icons/open-folder.png"
                }

                TapHandler {
                    enabled: isTreeNode && hasChildren
                    onSingleTapped: {
                        let index = treeView.index(row, column)
                        treeView.selectionModel.setCurrentIndex(index, ItemSelectionModel.NoUpdate)
                        treeView.toggleExpanded(row)
                    }
                }

            }
            // KLabel {
            //     id: indicator
            //     x: _delegate.padding + (depth * indentation)
            //     anchors.verticalCenter: parent.verticalCenter
            //     visible: isTreeNode && hasChildren
            //     text: "▶"

            //     TapHandler {
            //         onSingleTapped: {
            //             let index = treeView.index(row, column)
            //             treeView.selectionModel.setCurrentIndex(index, ItemSelectionModel.NoUpdate)
            //             treeView.toggleExpanded(row)
            //         }
            //     }
            // }

            KLabel {
                id: label
                x: _delegate.padding + (isTreeNode ? (depth + 1) * indentation : 0) + 6
                anchors.verticalCenter: parent.verticalCenter
                text: model.display
                rightPadding: _delegate.padding
            }

        }

        ScrollBar.vertical: ScrollBar {}
        ScrollBar.horizontal: ScrollBar {}
    }
}
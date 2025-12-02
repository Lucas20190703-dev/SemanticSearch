import QtQuick

ListModel {
    ListElement {
        iconSource: "qrc:/icons/search.png"
        name: qsTr("Search")                
    }
    ListElement {
        iconSource: "qrc:/icons/image.png"
        name: qsTr("Caption")                
    }
    ListElement {
        iconSource: "qrc:/icons/home.png"
        name: qsTr("Scene Detector")
    }

    ListElement {
        iconSource: "qrc:/icons/settings.png"
        name: qsTr("Settings")
    }

    ListElement {
        iconSource: "qrc:/icons/faq.png"
        name: qsTr("Help")
    }
}
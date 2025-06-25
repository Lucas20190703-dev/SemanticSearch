import QtQuick
import QtQuick.Controls
import KQuick.Controls

Item {
    id: _root

    property bool tintEnabled: true

    // property var icon: ({
    //     source: "",
    //     color: "white",
    //     width: 24,
    //     height: 24
    // })

    property KIconType icon : KIconType {}

    Image {
        id: _icon
        width: _root.icon.width
        height: _root.icon.height
        anchors.centerIn: parent
        source: _root.icon.source
        sourceSize: Qt.size(width * 2, height * 2)
        antialiasing: true
        fillMode: Image.PreserveAspectFit
        mipmap: true
        visible: false
    }

    ShaderEffect {
        anchors.fill: icon
        property var source: _icon
        property color tintColor: parent.tintColor

        fragmentShader: "
            uniform sampler2D source;
            uniform lowp vec4 tintColor;
            varying highp vec2 qt_TexCoord0;

            void main() {
                lowp vec4 tex = texture2D(source, qt_TexCoord0);
                gl_FragColor = vec4(tex.rgb * tintColor.rgb, tex.a * tintColor.a);
            }
        "
    }
}

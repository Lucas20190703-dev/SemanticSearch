pragma Singleton

import QtQuick

QtObject {
    readonly property string apiBase: "http://127.0.0.1:3000/api/"

    readonly property string apiMedia: apiBase + "media/"

    readonly property string apiSceneDetect: apiBase + "scene/"

    readonly property string apiCaption: apiBase + "caption?file="

    readonly property string apiRoot: apiBase + "directories"

    readonly property string apiFiles: apiBase + "files/" // api/files/subfolder?offset=0&limit=10

    readonly property string apiSearch: apiBase + "search"
    
    function mediaPath(file) {
        return apiMedia + removePrefix(file);
    }

    function removePrefix(file) {
        if (file && file.startsWith("file:///")) {
            return file.substring(8);
        }
        return file;
    }

    function parentPath(file) {
        return file.replace(/[/\\][^/\\]*$/, "");
    }

    function formatFileSize(bytes) {
        if (bytes === 0) return '0 B';
        const units = ['B', 'KB', 'MB', 'GB', 'TB', 'PB'];
        let i = 0;
        let size = bytes;
        while (size >= 1024 && i < units.length - 1) {
            size /= 1024;
            i++;
        }
        return size.toFixed(2) + ' ' + units[i];
    }

    function timestamp2Date(timestamp) {
        const date = new Date(timestamp * 1000)

        const year = date.getFullYear();
        const month = String(date.getMonth() + 1).padStart(2, '0');
        const day = String(date.getDate()).padStart(2, '0');

        const hours = String(date.getHours()).padStart(2, '0');
        const minutes = String(date.getMinutes()).padStart(2, '0');
        const seconds = String(date.getSeconds()).padStart(2, '0');

        const formatted = `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`;
        
        return formatted;
    }
}
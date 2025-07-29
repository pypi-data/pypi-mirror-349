"use strict";
(self["webpackChunkjupyterlab_unfold"] = self["webpackChunkjupyterlab_unfold"] || []).push([["lib_index_js"],{

/***/ "./lib/index.js":
/*!**********************!*\
  !*** ./lib/index.js ***!
  \**********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   DirTreeListing: () => (/* reexport safe */ _unfold__WEBPACK_IMPORTED_MODULE_6__.DirTreeListing),
/* harmony export */   FileTreeBrowser: () => (/* reexport safe */ _unfold__WEBPACK_IMPORTED_MODULE_6__.FileTreeBrowser),
/* harmony export */   FileTreeRenderer: () => (/* reexport safe */ _unfold__WEBPACK_IMPORTED_MODULE_6__.FileTreeRenderer),
/* harmony export */   FilterFileTreeBrowserModel: () => (/* reexport safe */ _unfold__WEBPACK_IMPORTED_MODULE_6__.FilterFileTreeBrowserModel),
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__),
/* harmony export */   folderOpenIcon: () => (/* reexport safe */ _unfold__WEBPACK_IMPORTED_MODULE_6__.folderOpenIcon)
/* harmony export */ });
/* harmony import */ var _jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/filebrowser */ "webpack/sharing/consume/default/@jupyterlab/filebrowser");
/* harmony import */ var _jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_docmanager__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/docmanager */ "webpack/sharing/consume/default/@jupyterlab/docmanager");
/* harmony import */ var _jupyterlab_docmanager__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_docmanager__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @jupyterlab/settingregistry */ "webpack/sharing/consume/default/@jupyterlab/settingregistry");
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @jupyterlab/translation */ "webpack/sharing/consume/default/@jupyterlab/translation");
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _jupyterlab_statedb__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @jupyterlab/statedb */ "webpack/sharing/consume/default/@jupyterlab/statedb");
/* harmony import */ var _jupyterlab_statedb__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_statedb__WEBPACK_IMPORTED_MODULE_5__);
/* harmony import */ var _unfold__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ./unfold */ "./lib/unfold.js");
/* eslint-disable @typescript-eslint/ban-ts-comment */







const SETTINGS_ID = 'jupyterlab-unfold:jupyterlab-unfold-settings';
/**
 * The file browser namespace token.
 */
const namespace = 'filebrowser';
const fileBrowserFactory = {
    id: 'jupyterlab-unfold:FileBrowserFactory',
    provides: _jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_0__.IFileBrowserFactory,
    requires: [_jupyterlab_docmanager__WEBPACK_IMPORTED_MODULE_1__.IDocumentManager, _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_4__.ITranslator, _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_3__.ISettingRegistry],
    optional: [_jupyterlab_statedb__WEBPACK_IMPORTED_MODULE_5__.IStateDB],
    activate: async (app, docManager, translator, settings, state) => {
        const setting = await settings.load(SETTINGS_ID);
        const tracker = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2__.WidgetTracker({ namespace });
        const createFileBrowser = (id, options = {}) => {
            var _a;
            const model = new _unfold__WEBPACK_IMPORTED_MODULE_6__.FilterFileTreeBrowserModel({
                translator: translator,
                auto: (_a = options.auto) !== null && _a !== void 0 ? _a : true,
                manager: docManager,
                driveName: options.driveName || '',
                refreshInterval: options.refreshInterval,
                state: options.state === null
                    ? undefined
                    : options.state || state || undefined
            });
            const widget = new _unfold__WEBPACK_IMPORTED_MODULE_6__.FileTreeBrowser({
                id,
                model,
                restore: true,
                translator,
                app
            });
            widget.listing.singleClickToUnfold = setting.get('singleClickToUnfold')
                .composite;
            setting.changed.connect(() => {
                widget.listing.singleClickToUnfold = setting.get('singleClickToUnfold')
                    .composite;
            });
            // check the url in iframe and open
            app.restored.then(async () => {
                const windowPathname = window.location.pathname;
                const treeIndex = windowPathname.indexOf('/tree/');
                let path = windowPathname.substring(treeIndex + '/tree/'.length);
                path = decodeURIComponent(path);
                const content = await app.serviceManager.contents.get(path);
                if (content.type !== 'directory') {
                    docManager.open(path);
                }
            });
            // Track the newly created file browser.
            void tracker.add(widget);
            return widget;
        };
        // @ts-ignore: DirListing._onPathChanged is private upstream, need to change this so we can remove the ignore
        return { createFileBrowser, tracker };
    }
};

/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (fileBrowserFactory);


/***/ }),

/***/ "./lib/unfold.js":
/*!***********************!*\
  !*** ./lib/unfold.js ***!
  \***********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   DirTreeListing: () => (/* binding */ DirTreeListing),
/* harmony export */   FileTreeBrowser: () => (/* binding */ FileTreeBrowser),
/* harmony export */   FileTreeRenderer: () => (/* binding */ FileTreeRenderer),
/* harmony export */   FilterFileTreeBrowserModel: () => (/* binding */ FilterFileTreeBrowserModel),
/* harmony export */   folderOpenIcon: () => (/* binding */ folderOpenIcon)
/* harmony export */ });
/* harmony import */ var _lumino_algorithm__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @lumino/algorithm */ "webpack/sharing/consume/default/@lumino/algorithm");
/* harmony import */ var _lumino_algorithm__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_lumino_algorithm__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _lumino_domutils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @lumino/domutils */ "webpack/sharing/consume/default/@lumino/domutils");
/* harmony import */ var _lumino_domutils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_lumino_domutils__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @lumino/coreutils */ "webpack/sharing/consume/default/@lumino/coreutils");
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_lumino_coreutils__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _jupyterlab_docmanager__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @jupyterlab/docmanager */ "webpack/sharing/consume/default/@jupyterlab/docmanager");
/* harmony import */ var _jupyterlab_docmanager__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_docmanager__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @jupyterlab/coreutils */ "webpack/sharing/consume/default/@jupyterlab/coreutils");
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_5__);
/* harmony import */ var _jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @jupyterlab/filebrowser */ "webpack/sharing/consume/default/@jupyterlab/filebrowser");
/* harmony import */ var _jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_6___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_6__);
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_7___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_7__);
/* harmony import */ var _style_icons_folder_open_svg__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! ../style/icons/folder-open.svg */ "./style/icons/folder-open.svg");
/* eslint-disable @typescript-eslint/ban-ts-comment */








// @ts-ignore

/**
 * The class name added to drop targets.
 */
const DROP_TARGET_CLASS = 'jp-mod-dropTarget';
/**
 * The mime type for a contents drag object.
 */
const CONTENTS_MIME = 'application/x-jupyter-icontents';
const folderOpenIcon = new _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_7__.LabIcon({
    name: 'ui-components:folder-open',
    svgstr: _style_icons_folder_open_svg__WEBPACK_IMPORTED_MODULE_8__
});
/**
 * A filetree renderer.
 */
class FileTreeRenderer extends _jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_6__.DirListing.Renderer {
    constructor(model) {
        super();
        this.model = model;
    }
    /**
     * Create the DOM node for a dir listing.
     */
    createNode() {
        const node = document.createElement('div');
        const content = document.createElement('ul');
        content.className = 'jp-DirListing-content';
        node.appendChild(content);
        node.tabIndex = 1;
        return node;
    }
    populateHeaderNode(node, translator, hiddenColumns) {
        // No-op we don't want any header
    }
    handleHeaderClick(node, event) {
        return null;
    }
    updateItemNode(node, model, fileType, translator, hiddenColumns, selected) {
        super.updateItemNode(node, model, fileType, translator, hiddenColumns, selected);
        if (model.type === 'directory' && this.model.isOpen(model.path)) {
            const iconContainer = _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_3__.DOMUtils.findElement(node, 'jp-DirListing-itemIcon');
            folderOpenIcon.element({
                container: iconContainer,
                className: 'jp-DirListing-itemIcon',
                stylesheet: 'listing'
            });
        }
        // Removing old vbars
        while (node.firstChild !== null &&
            node.firstChild.classList.contains('jp-DirListing-vbar')) {
            node.removeChild(node.firstChild);
        }
        // Adding vbars for subdirs
        for (let n = 0; n < model.path.split('/').length - 1; n++) {
            const vbar = document.createElement('div');
            vbar.classList.add('jp-DirListing-vbar');
            node.insertBefore(vbar, node.firstChild);
        }
    }
}
/**
 * A widget which hosts a filetree.
 */
// @ts-ignore: _onPathChanged is private upstream, need to change this
class DirTreeListing extends _jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_6__.DirListing {
    constructor(options) {
        super({ ...options, renderer: new FileTreeRenderer(options.model) });
        this._singleClickToUnfold = true;
    }
    set singleClickToUnfold(value) {
        this._singleClickToUnfold = value;
    }
    get headerNode() {
        return document.createElement('div');
    }
    sort(state) {
        // @ts-ignore
        this._sortedItems = (0,_lumino_algorithm__WEBPACK_IMPORTED_MODULE_0__.toArray)(this.model.items());
        // @ts-ignore
        this._sortState = state;
        this.update();
    }
    get model() {
        // @ts-ignore
        return this._model;
    }
    async _eventDblClick(event) {
        const entry = this.modelForClick(event);
        if ((entry === null || entry === void 0 ? void 0 : entry.type) === 'directory') {
            if (!this._singleClickToUnfold) {
                this.model.toggle(entry.path);
            }
        }
        else {
            super.handleEvent(event);
        }
    }
    _onPathChanged() {
        // It's a no-op to overwrite the base class behavior
        // We don't want to deselect everything when the path changes
    }
    _eventDragEnter(event) {
        if (event.mimeData.hasData(CONTENTS_MIME)) {
            // @ts-ignore
            const index = this._hitTestNodes(this._items, event);
            let target;
            if (index !== -1) {
                // @ts-ignore
                target = this._items[index];
            }
            else {
                target = event.target;
            }
            target.classList.add(DROP_TARGET_CLASS);
            event.preventDefault();
            event.stopPropagation();
        }
    }
    _eventDragOver(event) {
        event.preventDefault();
        event.stopPropagation();
        event.dropAction = event.proposedAction;
        const dropTarget = _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_3__.DOMUtils.findElement(this.node, DROP_TARGET_CLASS);
        if (dropTarget) {
            dropTarget.classList.remove(DROP_TARGET_CLASS);
        }
        // @ts-ignore
        const index = this._hitTestNodes(this._items, event);
        let target;
        if (index !== -1) {
            // @ts-ignore
            target = this._items[index];
        }
        else {
            target = event.target;
        }
        target.classList.add(DROP_TARGET_CLASS);
    }
    _eventDrop(event) {
        event.preventDefault();
        event.stopPropagation();
        // @ts-ignore
        clearTimeout(this._selectTimer);
        if (event.proposedAction === 'none') {
            event.dropAction = 'none';
            return;
        }
        if (!event.mimeData.hasData(CONTENTS_MIME)) {
            return;
        }
        let target = event.target;
        while (target && target.parentElement) {
            if (target.classList.contains(DROP_TARGET_CLASS)) {
                target.classList.remove(DROP_TARGET_CLASS);
                break;
            }
            target = target.parentElement;
        }
        // Get the path based on the target node.
        // @ts-ignore
        const index = _lumino_algorithm__WEBPACK_IMPORTED_MODULE_0__.ArrayExt.firstIndexOf(this._items, target);
        let newDir;
        if (index !== -1) {
            const item = (0,_lumino_algorithm__WEBPACK_IMPORTED_MODULE_0__.toArray)(this.model.items())[index];
            if (item.type === 'directory') {
                newDir = item.path;
            }
            else {
                newDir = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_5__.PathExt.dirname(item.path);
            }
        }
        else {
            newDir = '';
        }
        // @ts-ignore
        const manager = this._manager;
        // Handle the items.
        const promises = [];
        const paths = event.mimeData.getData(CONTENTS_MIME);
        if (event.ctrlKey && event.proposedAction === 'move') {
            event.dropAction = 'copy';
        }
        else {
            event.dropAction = event.proposedAction;
        }
        for (const path of paths) {
            const localPath = manager.services.contents.localPath(path);
            const name = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_5__.PathExt.basename(localPath);
            const newPath = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_5__.PathExt.join(newDir, name);
            // Skip files that are not moving.
            if (newPath === path) {
                continue;
            }
            if (event.dropAction === 'copy') {
                promises.push(manager.copy(path, newDir));
            }
            else {
                promises.push((0,_jupyterlab_docmanager__WEBPACK_IMPORTED_MODULE_4__.renameFile)(manager, path, newPath));
            }
        }
        Promise.all(promises).catch(error => {
            void (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_3__.showErrorMessage)(
            // @ts-ignore
            this._trans._p('showErrorMessage', 'Error while copying/moving files'), error);
        });
    }
    /**
     * Handle 'mousedown' event
     *
     * Note: This allow to change the path to the root and clear selection when the user
     * is clicking on an empty space.
     */
    _eventMouseDown(event) {
        const entry = this.modelForClick(event);
        if (entry) {
            if (entry.type === 'directory') {
                this.model.path = '/' + entry.path;
                if (this._singleClickToUnfold && event.button === 0) {
                    this.model.toggle(entry.path);
                }
            }
            else {
                this.model.path = '/' + _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_5__.PathExt.dirname(entry.path);
            }
        }
        else {
            // TODO Upstream this logic to JupyterLab (clearing selection when clicking the empty space)?
            this.clearSelectedItems();
            this.update();
            this.model.path = this.model.rootPath;
        }
    }
    _hitTestNodes(nodes, event) {
        return _lumino_algorithm__WEBPACK_IMPORTED_MODULE_0__.ArrayExt.findFirstIndex(nodes, node => _lumino_domutils__WEBPACK_IMPORTED_MODULE_1__.ElementExt.hitTest(node, event.clientX, event.clientY) ||
            event.target === node);
    }
    handleEvent(event) {
        switch (event.type) {
            case 'dblclick':
                this._eventDblClick(event);
                break;
            case 'lm-dragenter':
                this._eventDragEnter(event);
                break;
            case 'lm-dragover':
                this._eventDragOver(event);
                break;
            case 'lm-drop':
                this._eventDrop(event);
                break;
            case 'mousedown':
                super.handleEvent(event);
                this._eventMouseDown(event);
                break;
            default:
                super.handleEvent(event);
                break;
        }
    }
}
/**
 * Filetree browser model with optional filter on element.
 */
class FilterFileTreeBrowserModel extends _jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_6__.FilterFileBrowserModel {
    constructor(options) {
        super(options);
        this._isRestored = new _lumino_coreutils__WEBPACK_IMPORTED_MODULE_2__.PromiseDelegate();
        this._savedState = null;
        this._stateKey = null;
        this.openState = {};
        this.contentManager = this.manager.services.contents;
        this._savedState = options.state || null;
        this._path = this.rootPath;
    }
    get path() {
        return this._path;
    }
    set path(value) {
        let needsToEmit = false;
        if (this._path !== value) {
            needsToEmit = true;
        }
        const oldValue = this._path;
        this._path = value;
        if (needsToEmit) {
            const pathChanged = this.pathChanged;
            pathChanged.emit({
                name: 'path',
                oldValue,
                newValue: this._path
            });
        }
    }
    /**
     * Change directory.
     *
     * @param path - The path to the file or directory.
     *
     * @returns A promise with the contents of the directory.
     */
    async cd(pathToUpdate = this.rootPath) {
        const result = await this.fetchContent(this.rootPath, pathToUpdate);
        // @ts-ignore
        this.handleContents({
            name: this.rootPath,
            path: this.rootPath,
            type: 'directory',
            content: result
        });
        if (this._savedState && this._stateKey) {
            void this._savedState.save(this._stateKey, { openState: this.openState });
        }
        this.onRunningChanged(this.manager.services.sessions, this.manager.services.sessions.running());
    }
    /**
     * A promise that resolves when the model is first restored.
     */
    get restored() {
        return this._isRestored.promise;
    }
    /**
     * Restore the state of the file browser.
     *
     * @param id - The unique ID that is used to construct a state database key.
     *
     * @param populate - If `false`, the restoration ID will be set but the file
     * browser state will not be fetched from the state database.
     *
     * @returns A promise when restoration is complete.
     *
     * #### Notes
     * This function will only restore the model *once*. If it is called multiple
     * times, all subsequent invocations are no-ops.
     */
    async restore(id, populate = true) {
        const { manager } = this;
        const key = `file-browser-${id}:openState`;
        const state = this._savedState;
        const restored = !!this._stateKey;
        if (restored) {
            return;
        }
        // Set the file browser key for state database fetch/save.
        this._stateKey = key;
        if (!populate || !state) {
            this._isRestored.resolve(undefined);
            return;
        }
        await manager.services.ready;
        try {
            const value = await state.fetch(key);
            if (!value) {
                await this.cd(this.rootPath);
                this._isRestored.resolve(undefined);
                return;
            }
            this.openState = value['openState'];
            await this.cd(this.rootPath);
        }
        catch (error) {
            await this.cd(this.rootPath);
            await state.remove(key);
        }
        this._isRestored.resolve(undefined);
    }
    /**
     * Open/close directories to discover/hide a given path.
     *
     * @param pathToToggle - The path to discover/hide.
     */
    async toggle(pathToToggle = this.rootPath) {
        this.openState[pathToToggle] = !this.openState[pathToToggle];
        // Refresh
        this.cd(this.rootPath);
    }
    /**
     * Check whether a directory path is opened or not.
     *
     * @param path - The given path
     *
     * @returns Whether the directory is opened or not.
     *
     */
    isOpen(path) {
        return !!this.openState[path];
    }
    async fetchContent(path, pathToUpdate) {
        const result = await this.contentManager.get(path);
        if (!result.content) {
            return [];
        }
        let items = [];
        const sortedContent = this.sortContents(result.content);
        this.openState[path] = true;
        for (const entry of sortedContent) {
            items.push(entry);
            if (entry.type !== 'directory') {
                continue;
            }
            const isOpen = (pathToUpdate && pathToUpdate.startsWith('/' + entry.path)) ||
                this.isOpen(entry.path);
            if (isOpen) {
                const subEntryContent = await this.fetchContent(entry.path, pathToUpdate);
                items = items.concat(subEntryContent);
            }
            else {
                this.openState[entry.path] = false;
            }
        }
        return items;
    }
    /**
     * Sort the entries
     *
     * @param data: The entries to sort
     * @returns the sorted entries
     */
    sortContents(data) {
        const directories = data.filter(value => value.type === 'directory');
        const files = data.filter(value => value.type !== 'directory');
        const sortedDirectories = directories.sort((a, b) => a.name.localeCompare(b.name));
        const sortedFiles = files.sort((a, b) => a.name.localeCompare(b.name));
        return sortedDirectories.concat(sortedFiles);
    }
    onFileChanged(sender, change) {
        this.refresh();
    }
}
/**
 * The filetree browser.
 */
class FileTreeBrowser extends _jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_6__.FileBrowser {
    constructor(options) {
        var _a;
        super(options);
        (_a = this.mainPanel.layout) === null || _a === void 0 ? void 0 : _a.removeWidget(this.crumbs);
        this.showLastModifiedColumn = false;
        this.showFileCheckboxes = false;
    }
    get showFileCheckboxes() {
        return false;
    }
    set showFileCheckboxes(value) {
        if (this.listing.setColumnVisibility) {
            this.listing.setColumnVisibility('is_selected', false);
            // @ts-ignore
            this._showFileCheckboxes = false;
        }
    }
    get showLastModifiedColumn() {
        return false;
    }
    set showLastModifiedColumn(value) {
        if (this.listing.setColumnVisibility) {
            this.listing.setColumnVisibility('last_modified', false);
        }
    }
    createDirListing(options) {
        // @ts-ignore: _onPathChanged is private upstream, need to change this
        return new DirTreeListing({
            model: this.model,
            translator: this.translator
        });
    }
    set useFuzzyFilter(value) {
        // No-op
    }
}


/***/ }),

/***/ "./style/icons/folder-open.svg":
/*!*************************************!*\
  !*** ./style/icons/folder-open.svg ***!
  \*************************************/
/***/ ((module) => {

module.exports = "<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"16\" viewBox=\"0 0 576 512\"><path class=\"jp-icon3 jp-icon-selectable\" fill=\"#616161\" d=\"M572.694 292.093L500.27 416.248A63.997 63.997 0 0 1 444.989 448H45.025c-18.523 0-30.064-20.093-20.731-36.093l72.424-124.155A64 64 0 0 1 152 256h399.964c18.523 0 30.064 20.093 20.73 36.093zM152 224h328v-48c0-26.51-21.49-48-48-48H272l-64-64H48C21.49 64 0 85.49 0 112v278.046l69.077-118.418C86.214 242.25 117.989 224 152 224z\"></path></svg>\n";

/***/ })

}]);
//# sourceMappingURL=lib_index_js.6dfa3f02b6bc6bc819cd.js.map
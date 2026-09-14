// ExtendScript ES3. Only explicit create/open calls grant document ownership.
var IllustratorSession = (function () {
    var api = {current: null};
    function fileOK(path) { var f = File(path); return f.exists && f.length > 0; }
    function canonical(path) { var f = File(path); if (f.alias) f = f.resolve(); return f.fsName; }
    function begin(options) {
        var baseline = [], owned = [], oldInteraction = app.userInteractionLevel;
        var previous = app.documents.length ? app.activeDocument : null;
        var recovery = Folder(options.recoveryDir), notes = [], finished = false;
        if (!recovery.exists) throw Error('Create recoveryDir before running Illustrator.');
        for (var i = 0; i < app.documents.length; i++) baseline.push(app.documents[i]);
        function mark(note) { if(options.progressPath) {var f=File(options.progressPath); if(f.open('w')) {f.write(note);f.close();}} }
        function entry(doc) {
            for (var i = 0; i < owned.length; i++) if (owned[i].doc === doc) return owned[i];
            throw Error('Document is not owned by this session.');
        }
        function register(doc, mode) {
            for (var i = 0; i < baseline.length; i++) if (baseline[i] === doc) throw Error('Pre-existing document is protected.');
            owned.push({doc:doc, mode:mode, ai:null}); return doc;
        }
        function create(space, width, height) { mark('create: before native add'); var doc=app.documents.add(space,width,height); mark('create: before ownership registration'); register(doc,'work'); mark('create: registered'); return doc; }
        function open(path, mode) {
            if (mode !== 'read' && mode !== 'work') throw Error('Specify read or work mode.');
            var target = canonical(path);
            if (!fileOK(target)) throw Error('Missing or empty input: ' + target);
            for (var i = 0; i < app.documents.length; i++) {
                var existing = null;
                try { existing = canonical(app.documents[i].fullName); } catch (_) {}
                if (existing === target) throw Error('Input already open; preserve that tab: ' + target);
            }
            return register(app.open(File(target)), mode);
        }
        function checkpoint(doc, aiPath) {
            var e = entry(doc);
            if (!/\.ai$/i.test(aiPath) || !fileOK(aiPath) || !doc.saved || canonical(doc.fullName) !== canonical(aiPath))
                throw Error('AI checkpoint must follow a successful native saveAs.');
            e.ai = canonical(aiPath);
        }
        function saveOutputs(doc, aiPath, pdfPath, range) {
            entry(doc);
            var aiFile = File(aiPath), pdfFile = pdfPath ? File(pdfPath) : null;
            if (!/\.ai$/i.test(aiPath) || (pdfPath && !/\.pdf$/i.test(pdfPath))) throw Error('Require .ai and optional .pdf output paths.');
            if (aiFile.exists || (pdfFile && pdfFile.exists)) throw Error('Output exists; choose a fresh version.');
            if (!aiFile.parent.exists || (pdfFile && !pdfFile.parent.exists)) throw Error('Create output directories first.');
            var ao = new IllustratorSaveOptions(); ao.pdfCompatible = true; ao.compressed = true; ao.embedLinkedFiles = true;
            doc.saveAs(aiFile, ao); checkpoint(doc, aiPath);
            if (pdfFile) {
                var po = new PDFSaveOptions(); po.preserveEditability = false; po.viewAfterSaving = false;
                if (range) po.artboardRange = range;
                doc.saveAs(pdfFile, po);
                if (!fileOK(pdfPath)) throw Error('PDF is missing or empty after export.');
            }
        }
        function placeLinked(doc, layer, path, box) {
            entry(doc);
            if (!box || box.length !== 4 || !(box[2] > 0) || !(box[3] > 0)) throw Error('Specify [left, top, width, height] in Illustrator coordinates.');
            if (!fileOK(path)) throw Error('Missing image: ' + path);
            var item = layer.placedItems.add(); item.file = File(path);
            item.width = box[2]; item.height = box[3]; item.position = [box[0], box[1]];
            return item; // Save embeds links; no destructive embed() during construction.
        }
        function textSummary(doc) {
            entry(doc);
            var rows = [], count = doc.textFrames.length;
            for (var i = 0; i < count; i++) {
                var t = doc.textFrames[i];
                rows.push({index:i, contents:String(t.contents), kind:String(t.kind), bounds:[t.geometricBounds[0],t.geometricBounds[1],t.geometricBounds[2],t.geometricBounds[3]]});
            }
            return rows; // Plain JS data; safe to log after the document is closed.
        }
        function close(doc) {
            var e = entry(doc);
            if (!doc.saved) throw Error('Unsaved document; checkpoint it or let recovery handle it.');
            if (e.mode === 'work' && (!e.ai || !fileOK(e.ai))) throw Error('Native AI checkpoint required before closing.');
            doc.close(SaveOptions.DONOTSAVECHANGES);
            e.doc = null; // Never access a closed host object again.
        }
        function finish() {
            if (finished) return notes; finished = true;
            var errors = [];
            try {
                for (var i = owned.length - 1; i >= 0; i--) {
                    var e = owned[i]; if (!e.doc) continue;
                    try {
                        if (!e.doc.saved || (e.mode === 'work' && (!e.ai || !fileOK(e.ai)))) {
                            var f = File(recovery.fsName + '/recovered-' + (new Date().getTime()) + '-' + i + '.ai');
                            if (f.exists) throw Error('Recovery path exists: ' + f.fsName);
                            var opts = new IllustratorSaveOptions(); opts.pdfCompatible = true; opts.compressed = true; opts.embedLinkedFiles = true;
                            e.doc.saveAs(f, opts);
                            checkpoint(e.doc, f.fsName);
                            e.mode = 'work';
                            notes.push('RECOVERED ' + f.fsName);
                        }
                        close(e.doc);
                    } catch (err) {
                        // Do not discard unsaved work when saving/closing fails.
                        errors.push('RETAINED owned document ' + i + ': ' + err);
                    }
                }
                // Detect, but do not adopt, tabs opened by unadapted scripts or the user.
                for (var j = 0; j < app.documents.length; j++) {
                    var known = false;
                    for (var k = 0; k < baseline.length; k++) if (baseline[k] === app.documents[j]) known = true;
                    for (var k = 0; k < owned.length; k++) if (owned[k].doc === app.documents[j]) known = true;
                    if (!known) errors.push('UNTRACKED document left open; use session.create/open.');
                }
            } finally {
                app.userInteractionLevel = oldInteraction;
                // Restore only if the old document is still in the live collection.
                if (previous) for (var n = 0; n < app.documents.length; n++) {
                    if (app.documents[n] === previous) { try { previous.activate(); } catch (_) {} break; }
                }
            }
            if (errors.length) throw Error(errors.join('\n') + '\n' + notes.join('\n'));
            return notes;
        }
        return {mark:mark, create:create, open:open, checkpoint:checkpoint, saveOutputs:saveOutputs, placeLinked:placeLinked, textSummary:textSummary, close:close, finish:finish, notes:notes};
    }
    api.run = function (options, callback) {
        if (api.current) throw Error('Nested Illustrator sessions are not allowed.');
        var s = begin(options), result, problem = null, cleanupProblem = null;
        api.current = s;
        try {
            app.userInteractionLevel = options.interactionLevel === undefined ? UserInteractionLevel.DONTDISPLAYALERTS : options.interactionLevel;
            result = callback(s);
        } catch (err) { problem = err; }
        finally {
            try { s.finish(); } catch (err) { cleanupProblem = err; }
            api.current = null;
        }
        if (problem || cleanupProblem) throw Error((problem ? String(problem) + ' line ' + problem.line : '') + '\n' + (cleanupProblem || '') + '\n' + s.notes.join('\n'));
        if (s.notes.length) throw Error('Output incomplete; work saved for recovery.\n' + s.notes.join('\n'));
        return result;
    };
    return api;
}());

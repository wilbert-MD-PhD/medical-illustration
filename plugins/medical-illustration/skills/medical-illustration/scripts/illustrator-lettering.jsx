// MIT License; see ../LICENSE-CODE.
// Illustrator ExtendScript library. Loading this file does not modify documents.
// Coordinates are points from the current page's upper-left corner.
var ComicPage = (function () {
    function color(hex) {
        var c = new RGBColor();
        c.red = parseInt(hex.substr(0, 2), 16);
        c.green = parseInt(hex.substr(2, 2), 16);
        c.blue = parseInt(hex.substr(4, 2), 16);
        return c;
    }
    function create(options) {
        if (!options || !(options.width > 0) || !(options.height > 0)) throw Error('Specify page width and height in points.');
        var W = options.width, H = options.height, X = 0, pages = [], rows = [];
        var regular = app.textFonts.getByName(options.fontRegular || 'LXGWWenKai-Regular');
        var medium = app.textFonts.getByName(options.fontMedium || 'LXGWWenKai-Medium');
        var doc = app.documents.add(DocumentColorSpace.RGB, W, H);
        var art = doc.layers[0]; art.name = '原始无字画面';
        var bubbles = doc.layers.add(); bubbles.name = '半透明气泡';
        var labels = doc.layers.add(); labels.name = '医学标签与箭头';
        var body = doc.layers.add(); body.name = '可编辑文字';
        function requirePage() { if (!pages.length) throw Error('Create a page first.'); }
        function path(points, layer) {
            requirePage();
            var p = layer.pathItems.add(), transformed = [];
            for (var i = 0; i < points.length; i++) transformed.push([X + points[i][0], H - points[i][1]]);
            p.setEntirePath(transformed);
            return p;
        }
        function page(id, imagePath) {
            if (!id) throw Error('A stable page id is required for records.');
            for (var i = 0; i < pages.length; i++) if (pages[i].id == id) throw Error('Duplicate page id.');
            var f = imagePath ? File(imagePath) : null;
            if (f && !f.exists) throw Error('Missing image: ' + imagePath);
            X = pages.length * (W + 20);
            if (pages.length) doc.artboards.add([X, H, X + W, 0]);
            doc.artboards.setActiveArtboardIndex(pages.length);
            doc.artboards[pages.length].name = id; // Internal metadata; never printed.
            pages.push({id: id, image: imagePath || null});
            if (f) {
                var item = art.placedItems.add(); item.file = f;
                if (Math.abs((item.width / item.height) / (W / H) - 1) > 0.005) {
                    item.remove();
                    throw Error('Image/page aspect ratio differs. Design the crop explicitly; do not stretch anatomy.');
                }
                item.width = W; item.height = H; item.position = [X, H]; item.embed();
            }
            return doc.artboards[pages.length - 1];
        }
        function text(str, x, baseline, o) {
            requirePage(); o = o || {};
            var t = (o.label ? labels : body).textFrames.add();
            t.contents = str.replace(/\n/g, '\r'); t.position = [X + x, H - baseline];
            var a = t.textRange.characterAttributes;
            a.textFont = o.bold ? medium : regular; a.size = o.size || 11;
            a.fillColor = color(o.color || '344E54'); a.autoLeading = false;
            a.leading = o.leading || a.size * 1.3;
            t.opacity = 100;
            rows.push({page: pages[pages.length - 1].id, text: str, x: x, baseline: baseline, size: a.size});
            return t;
        }
        function line(points, o) {
            o = o || {}; var p = path(points, labels);
            p.filled = false; p.stroked = true; p.strokeColor = color(o.color || '52827C');
            p.strokeWidth = o.width || 0.8; p.opacity = 100; return p;
        }
        function bubble(str, box, tip, o) {
            requirePage(); o = o || {};
            var opacity = o.fillOpacity === undefined ? 60 : o.fillOpacity;
            if (!(opacity > 0 && opacity < 100)) throw Error('Bubble fillOpacity must be between 0 and 100.');
            var x = box[0], y = box[1], w = box[2], h = box[3];
            if (!(w > 24 && h > 12)) throw Error('Bubble is too small.');
            var pts = [[x,y]], tx;
            if (tip && tip[1] > y && tip[1] < y+h) throw Error('Tail tip must be above or below the bubble.');
            if (tip) tx = Math.max(x+10,Math.min(x+w-10,tip[0]));
            if (tip && tip[1] <= y) pts = pts.concat([[tx-5,y],[tip[0],tip[1]],[tx+5,y]]);
            pts = pts.concat([[x+w,y],[x+w,y+h]]);
            if (tip && tip[1] >= y+h) pts = pts.concat([[tx+5,y+h],[tip[0],tip[1]],[tx-5,y+h]]);
            pts.push([x,y+h]);
            var fill = path(pts,bubbles); fill.closed = true; fill.filled = true;
            fill.fillColor = color(o.fill || 'FFFDF7'); fill.stroked = false; fill.opacity = opacity;
            // One outline includes the tail: no overlapping translucent tail fill.
            var outline = fill.duplicate(); outline.filled = false; outline.stroked = true;
            outline.strokeColor = color(o.stroke || '7D8580'); outline.strokeWidth = o.strokeWidth || 0.65; outline.opacity = 100;
            var size = o.size || 11, leading = o.leading || size*1.3, lines = str.split('\n');
            var baseline = y + (h - lines.length*leading)/2 + size;
            var frames = [];
            for (var k=0;k<lines.length;k++) {
                var t = text(lines[k],x+9,baseline+k*leading,{size:size,leading:leading,color:o.color});
                t.position = [X+x+(w-t.width)/2,H-baseline-k*leading];
                rows[rows.length-1].x = x+(w-t.width)/2;
                if (t.width > w-12) throw Error('Bubble text too wide; add a deliberate line break or enlarge its box.');
                frames.push(t);
            }
            if (lines.length*leading > h-8) throw Error('Bubble text too tall.');
            return {fill:fill,outline:outline,text:frames};
        }
        function save(aiPath, pdfPath) {
            requirePage();
            if (!aiPath || !/\.ai$/i.test(aiPath)) throw Error('An .ai source path is required.');
            if (pdfPath && !/\.pdf$/i.test(pdfPath)) throw Error('PDF output must use .pdf.');
            if (File(aiPath).exists || (pdfPath && File(pdfPath).exists)) throw Error('Output exists; choose a new version.');
            if (!File(aiPath).parent.exists || (pdfPath && !File(pdfPath).parent.exists)) throw Error('Create output folders first.');
            art.locked = true;
            var ai = new IllustratorSaveOptions(); ai.pdfCompatible = true; ai.embedLinkedFiles = true;
            doc.saveAs(File(aiPath), ai);
            if (pdfPath) {
                var pdf = new PDFSaveOptions(); pdf.preserveEditability = false;
                pdf.artboardRange = '1-' + pages.length;
                doc.saveAs(File(pdfPath), pdf);
            }
        }
        return {doc:doc,page:page,text:text,line:line,bubble:bubble,save:save,pages:pages,textRecords:rows};
    }
    return {create:create};
}());

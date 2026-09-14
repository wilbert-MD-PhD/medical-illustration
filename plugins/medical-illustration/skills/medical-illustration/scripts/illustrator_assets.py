#!/usr/bin/env python3
# MIT License; see ../LICENSE-CODE.
"""Lossless crop preparation for rectangular masked raster placements. Originals untouched."""
import argparse, hashlib, io, json, math
from pathlib import Path
from PIL import Image

def crop_asset(source, canvas, clip, output):
    source=Path(source).resolve();raw=source.read_bytes();digest=hashlib.sha256(raw).hexdigest()
    cw,ch=canvas;x,y,w,h=clip
    if not all(math.isfinite(v) for v in [cw,ch,x,y,w,h]) or min(cw,ch,w,h)<=0 or x<0 or y<0 or x+w>cw or y+h>ch:raise ValueError('Invalid page/clip bounds')
    with Image.open(io.BytesIO(raw)) as im:
        if im.mode not in ('RGB','RGBA','L','LA'):raise ValueError('Unsupported color mode; preserve source and handle explicitly: '+im.mode)
        iw,ih=im.size
        # Two pixels outside the mask preserve interpolation at the clipped edge.
        box=(max(0,math.floor(x/cw*iw)-2),max(0,math.floor(y/ch*ih)-2),min(iw,math.ceil((x+w)/cw*iw)+2),min(ih,math.ceil((y+h)/ch*ih)+2))
        cropped=im.crop(box);key=hashlib.sha256((digest+str(box)).encode()).hexdigest()[:20]
        output=Path(output);output.mkdir(parents=True,exist_ok=True);dest=output/(key+'.png')
        if not dest.exists():
            with dest.open('xb') as f:cropped.save(f,format='PNG',icc_profile=im.info.get('icc_profile'),dpi=im.info.get('dpi',(72,72)))
        with Image.open(dest) as actual:
            if actual.mode!=cropped.mode or actual.size!=cropped.size or actual.tobytes()!=cropped.tobytes():raise ValueError('Crop pixel mismatch')
            if actual.info.get('icc_profile')!=im.info.get('icc_profile'):raise ValueError('ICC profile mismatch')
        left,top,right,bottom=box
        return {'source':str(source),'source_sha256':digest,'path':str(dest.resolve()),'crop_sha256':hashlib.sha256(dest.read_bytes()).hexdigest(),'source_px':[iw,ih],'crop_px':list(cropped.size),'pixel_box':list(box),'clip_box_pt':clip,'place_box_pt':[left/iw*cw,top/ih*ch,(right-left)/iw*cw,(bottom-top)/ih*ch],'original_pixels':iw*ih,'cropped_pixels':cropped.width*cropped.height,'pixel_exact':True}


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('source',type=Path)
    p.add_argument('--canvas',type=float,nargs=2,required=True,metavar=('WIDTH','HEIGHT'))
    p.add_argument('--clip',type=float,nargs=4,required=True,metavar=('X','Y','WIDTH','HEIGHT'))
    p.add_argument('--output',type=Path,required=True,help='Directory for verified crop PNGs')
    a=p.parse_args()
    result=crop_asset(a.source,a.canvas,a.clip,a.output)
    print(json.dumps(result,ensure_ascii=False,indent=2))

if __name__=='__main__':
    main()

def build_comic_layout(outline, story, image_paths):
    if not (len(outline)==len(story)==len(image_paths)): raise ValueError("Panel counts do not match.")
    return [{**o, **{"image_path":img,"caption":s.get("caption",""),"narration":s.get("narration","")}}
            for o,s,img in zip(outline,story,image_paths)]

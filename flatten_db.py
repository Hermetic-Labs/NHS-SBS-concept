import json
import os
import glob

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(base_dir, 'data')
    out_file = os.path.join(base_dir, 'frontend', 'flattened_db.json')
    
    db = []
    
    # 1. Load CQs
    cq_file = os.path.join(data_dir, 'cq_index.json')
    if os.path.exists(cq_file):
        with open(cq_file, 'r', encoding='utf-8') as f:
            cqs = json.load(f)
            for cq in cqs:
                db.append({
                    "type": "cq",
                    "title": f"Question {cq.get('Question_Number', 'N/A')}",
                    "content": f"Q: {cq.get('Question', '')}\nA: {cq.get('Answer', '')}"
                })
    
    # 2. Load Markdown
    md_dir = os.path.join(data_dir, 'markdown_docs')
    if os.path.exists(md_dir):
        for md_path in glob.glob(os.path.join(md_dir, '*.md')):
            filename = os.path.basename(md_path)
            with open(md_path, 'r', encoding='utf-8') as f:
                content = f.read()
                # Split roughly by double newlines or headers to create smaller chunks
                chunks = content.split('\n\n')
                current_chunk = ""
                for chunk in chunks:
                    if len(current_chunk) + len(chunk) > 1000:
                        db.append({
                            "type": "doc",
                            "title": filename,
                            "content": current_chunk.strip()
                        })
                        current_chunk = chunk
                    else:
                        current_chunk += "\n\n" + chunk
                if current_chunk:
                    db.append({
                        "type": "doc",
                        "title": filename,
                        "content": current_chunk.strip()
                    })
                    
    # Write to frontend
    with open(out_file, 'w', encoding='utf-8') as f:
        json.dump(db, f, indent=2)
        
    print(f"Flattened DB created with {len(db)} entries at {out_file}")

if __name__ == '__main__':
    main()

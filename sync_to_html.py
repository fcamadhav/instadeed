def main():
    with open('test_script.jsx', 'r', encoding='utf-8') as f:
        jsx_content = f.read()

    with open('Madhav_Drafting_Hub.html', 'r', encoding='utf-8') as f:
        html_content = f.read()

    start_tag = '<script type="text/babel">'
    end_tag = '</script>'

    start_idx = html_content.find(start_tag)
    if start_idx == -1:
        print("Error: Could not find <script type=\"text/babel\"> start tag.")
        return

    end_idx = html_content.find(end_tag, start_idx)
    if end_idx == -1:
        print("Error: Could not find </script> end tag.")
        return

    new_html = html_content[:start_idx + len(start_tag)] + jsx_content + html_content[end_idx:]

    with open('Madhav_Drafting_Hub.html', 'w', encoding='utf-8') as f:
        f.write(new_html)
    print("Successfully synchronized test_script.jsx back to Madhav_Drafting_Hub.html using string slicing.")

if __name__ == '__main__':
    main()

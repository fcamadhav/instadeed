with open("landing.html", "r", encoding="utf-8") as f:
    content = f.read()

start_marker = "<!-- User chip (shown after sign-in) -->"
end_marker = "<!-- User dropdown -->"

start_idx = content.find(start_marker)
if start_idx == -1:
    print("Start marker not found")
    exit(1)

# Find the userMenu block end. We know it starts with <div id="userMenu" or class="user-menu" and ends with a closing </div>.
# Let's locate the next occurrences of </div> after start_idx.
# To be robust, let's find the closing </div> of the dropdown.
dropdown_start = content.find("id=\"userMenu\"", start_idx)
if dropdown_start == -1:
    dropdown_start = content.find("class=\"user-menu\"", start_idx)

if dropdown_start == -1:
    print("Dropdown block not found")
    exit(1)

# Find the matching closing </div> of the dropdown (it's the first </div> after userMenuEmail links)
dropdown_end = content.find("</div>", content.find("Sign out", dropdown_start))
if dropdown_end == -1:
    print("Closing div not found")
    exit(1)

end_idx = dropdown_end + len("</div>")

print(f"Replacing content from index {start_idx} to {end_idx}...")
print("Original segment:")
print(content[start_idx:end_idx])

new_user_block = """<!-- User chip (shown after sign-in) -->
<div class="user-chip" id="userChip" onclick="toggleUserMenu()">
  <div class="user-avatar" id="userAvatar">U</div>
  <span class="user-name" id="userName">User</span>
  <i class="fa-solid fa-chevron-down" style="font-size:.55rem;margin-left:.15rem"></i>
</div>
<!-- User dropdown -->
<div class="user-menu" id="userMenu" style="display:none;">
  <div class="user-menu-header" id="userMenuEmail"></div>
  <div class="user-menu-item" onclick="scrollToSection('pricing')">
    <i class="fa-solid fa-file-contract" style="color:var(--blue-l);width:14px;margin-right:0.5rem;"></i> My Documents
  </div>
  <div class="user-menu-item" style="color:var(--rose);" onclick="signOut()">
    <i class="fa-solid fa-right-from-bracket" style="color:var(--rose);width:14px;margin-right:0.5rem;"></i> Sign out
  </div>
</div>"""

new_content = content[:start_idx] + new_user_block + content[end_idx:]

with open("landing.html", "w", encoding="utf-8") as f:
    f.write(new_content)

print("Replacement successful!")
print(f"class=\"user-menu\" in file: {'class=\"user-menu\"' in open('landing.html', 'r', encoding='utf-8').read()}")

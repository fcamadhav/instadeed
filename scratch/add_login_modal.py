import re

hub_file = 'Madhav_Drafting_Hub.html'

with open(hub_file, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Define the LoginModal component before ShareModal definition
target_sharemodal = "        const ShareModal = ({ isOpen, onClose, data, onImport }) => {"
login_modal_definition = """        const LoginModal = ({ isOpen, onClose, onLogin }) => {
            React.useEffect(() => {
                if (!isOpen) return;
                
                const initGoogle = () => {
                    if (window.google && window.google.accounts && window.google.accounts.id) {
                        window.google.accounts.id.initialize({
                            client_id: "92873092183-sampleclientid.apps.googleusercontent.com",
                            callback: (response) => {
                                try {
                                    const base64Url = response.credential.split('.')[1];
                                    const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
                                    const jsonPayload = decodeURIComponent(window.atob(base64).split('').map(c => '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2)).join(''));
                                    const payload = JSON.parse(jsonPayload);
                                    const userSession = {
                                        name: payload.name,
                                        email: payload.email,
                                        picture: payload.picture
                                    };
                                    localStorage.setItem('instadeed_user_session', JSON.stringify(userSession));
                                    onLogin(userSession);
                                    onClose();
                                } catch (err) {
                                    console.error("Auth error:", err);
                                }
                            }
                        });
                        window.google.accounts.id.renderButton(
                            document.getElementById("google-signin-btn-hub"),
                            { theme: "outline", size: "large", width: 280 }
                        );
                    }
                };

                initGoogle();
                const interval = setInterval(() => {
                    if (window.google && window.google.accounts && window.google.accounts.id) {
                        initGoogle();
                        clearInterval(interval);
                    }
                }, 500);

                return () => clearInterval(interval);
            }, [isOpen]);

            if (!isOpen) return null;

            const triggerMock = () => {
                const mockUser = {
                    name: "Demo Signee",
                    email: "signee@instadeed.com",
                    picture: "https://www.gravatar.com/avatar/00000000000000000000000000000000?d=mp&f=y"
                };
                localStorage.setItem('instadeed_user_session', JSON.stringify(mockUser));
                onLogin(mockUser);
                onClose();
                alert("Signed in successfully as " + mockUser.name);
            };

            return (
                <div
                    className="fixed inset-0 bg-black/60 z-[9999] flex items-center justify-center p-4 backdrop-blur-sm transition-all"
                    onClick={onClose}
                >
                    <div
                        className="bg-[#FCFAF5] w-full max-w-sm p-2 border-2 border-[#D8C7A5] relative animate-in fade-in zoom-in duration-200"
                        onClick={(e) => e.stopPropagation()}
                    >
                        <div className="border border-[#D8C7A5] p-6 relative flex flex-col items-center">
                            <button
                                onClick={onClose}
                                className="absolute top-2 right-2 text-xl font-bold text-gray-800 hover:text-red-500 transition-colors"
                            >
                                ×
                            </button>
                            
                            <div className="mb-6 text-center w-full border-b border-[#D8C7A5] pb-4">
                                <h3 className="font-serif text-xl font-bold text-gray-800 uppercase tracking-widest">Signee Access</h3>
                            </div>

                            <div className="space-y-4 w-full flex flex-col items-center">
                                <div id="google-signin-btn-hub" className="w-full flex justify-center py-1 min-h-[40px]"></div>
                                
                                <div className="w-full text-center text-xs text-gray-400 font-serif my-2">— OR —</div>

                                <button
                                    onClick={triggerMock}
                                    className="w-full py-3 bg-transparent border border-gray-800 hover:bg-gray-800 hover:text-[#FCFAF5] text-gray-800 transition-all uppercase font-semibold text-xs tracking-wider"
                                >
                                    Access via Google (Mock)
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            );
        };

        const ShareModal = ({ isOpen, onClose, data, onImport }) => {"""

if target_sharemodal in content:
    content = content.replace(target_sharemodal, login_modal_definition)
    print("1. LoginModal definition injected successfully.")
else:
    print("Error: target_sharemodal not found.")

# 2. Add showLogin state in Home component
target_state = """            const [activeAuthority, setActiveAuthority] = useState('ALL');
            const [user, setUser] = useState(null);"""

replacement_state = """            const [activeAuthority, setActiveAuthority] = useState('ALL');
            const [user, setUser] = useState(null);
            const [showLogin, setShowLogin] = useState(false);"""

if target_state in content:
    content = content.replace(target_state, replacement_state)
    print("2. showLogin state added successfully.")
else:
    print("Error: target_state not found.")

# 3. Replace the Sign In button click handler to open the LoginModal
target_btn = """                                    ) : (
                                        <button onClick={() => {
                                            const mockUser = {
                                                name: "Demo Signee",
                                                email: "signee@instadeed.com",
                                                picture: "https://www.gravatar.com/avatar/00000000000000000000000000000000?d=mp&f=y"
                                            };
                                            localStorage.setItem('instadeed_user_session', JSON.stringify(mockUser));
                                            setUser(mockUser);
                                            alert("Signed in successfully as " + mockUser.name);
                                        }} className="text-[10px] uppercase font-bold text-slate-500 hover:text-indigo-600 border border-slate-200 rounded-full px-2.5 py-1 transition bg-slate-50" title="Sign In (Mock)">
                                            Sign In
                                        </button>
                                    )}"""

replacement_btn = """                                    ) : (
                                        <button onClick={() => setShowLogin(true)} className="text-[10px] uppercase font-bold text-slate-500 hover:text-indigo-600 border border-slate-200 rounded-full px-2.5 py-1 transition bg-slate-50" title="Sign In">
                                            Sign In
                                        </button>
                                    )}"""

if target_btn in content:
    content = content.replace(target_btn, replacement_btn)
    print("3. Sign In button click handler updated successfully.")
else:
    print("Error: target_btn not found exactly.")

# 4. Render LoginModal inside Home return block (next to ShareModal)
target_render = """                        {/* Share Modal */}
                        <ShareModal"""

replacement_render = """                        {/* Login Modal */}
                        <LoginModal
                            isOpen={showLogin}
                            onClose={() => setShowLogin(false)}
                            onLogin={setUser}
                        />

                        {/* Share Modal */}
                        <ShareModal"""

if target_render in content:
    content = content.replace(target_render, replacement_render)
    print("4. LoginModal rendering injected successfully.")
else:
    print("Error: target_render not found.")

with open(hub_file, 'w', encoding='utf-8') as f:
    f.write(content)

print("All login modal updates processed successfully!")

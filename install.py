import time

try:
    import os
    import sys
    # Get the required directories
    frontendDirectory = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Frontend')
    assetsDirectory = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Assets')
    # Add the Frontend directory to sys.path
    sys.path.append(frontendDirectory)
    sys.path.append(assetsDirectory)
    os.chdir(frontendDirectory)
    # Install dependencies
    try:
        os.system('pip install customtkinter tk packaging Pillow')
    except:
        try:
            os.system('pip3 install customtkinter tk packaging Pillow')
        except:
            try:
                os.system('python -m pip install customtkinter tk packaging Pillow')
            except:
                try:
                    os.system('python -m pip3 install customtkinter tk packaging Pillow')
                except:
                    print('Failed to install dependencies')
                    exit()


    #The main wizard
    import customtkinter as ctk
    from tkinter.filedialog import askdirectory
    from photo_object import Photo
    os.chdir(assetsDirectory)

    root = ctk.CTk()
    root.title('Installation Kitten')
    root.geometry('500x300')
    root.resizable(False, False)
    root.iconbitmap('Logo.ico')

    def openFile():
        try:
            root.destroy()
            os.chdir(frontendDirectory)
            os.system('python Purrfect_Tube_Downloader.py')
        except:
            try:
                import platform, subprocess
                system_platform = platform.system()
                if system_platform == "Darwin":  # macOS
                    subprocess.run(["open", os.path.join(frontendDirectory, 'Purrfect_Tube_Downloader.py')])
                    root.destroy()
            except:
                try:
                    os.system('python -m Purrfect_Tube_Downloader.py')
                    root.destroy()
                except:
                    try:
                        import platform, subprocess
                        system_platform = platform.system()
                        if system_platform == "Darwin":  # macOS
                            subprocess.run(["open", os.path.join(frontendDirectory, 'Purrfect_Tube_Downloader.py')])
                            root.destroy()
                    except:
                        progressLabel.configure(text='Failed to open, open the Frontend folder and open manually')

                        progressLabel.place(relx=0.5, anchor='center')
                        return False

    def install():
        os.chdir(frontendDirectory)
        installButton.place_forget()
        success=0
        progressLabel.place(relx=0.5, rely=0.85, anchor='center')
        try:
            progressLabel.configure(text='Installing...')
            time.sleep(1)
            os.system('pip install -r requirements.txt')
            success=1
        except:
            try:
                progressLabel.configure(text='Installing...')
                time.sleep(1)
                os.system('pip3 install -r requirements.txt')
                success=1
            except:
                try:
                    progressLabel.configure(text='Installing...')
                    time.sleep(1)
                    os.system('python -m pip install -r requirements.txt')
                    success=1
                except:
                    try:
                        progressLabel.configure(text='Installing...')
                        time.sleep(1)
                        os.system('python -m pip3 install -r requirements.txt')
                        success=1
                    except:
                        progressLabel.configure(text='Failed to install dependencies')
                        success=0
        if success==0:
            progressLabel.configure(text='Failed to install, try again or contact developer')

        elif success==1:
            def create_shortcut_windows(target_file, shortcut_location, shortcut_name):
                try:
                    os.system('pip install pywin32')
                    import win32com.client
                    # Create a shortcut (.lnk) file
                    shortcut_path = os.path.join(shortcut_location, f"{shortcut_name}.lnk")
                    # Create a ShellLink object
                    shell = win32com.client.Dispatch("WScript.Shell")
                    shortcut = shell.CreateShortCut(shortcut_path)
                    # Set the target of the shortcut
                    shortcut.Targetpath = target_file
                    shortcut.WorkingDirectory = frontendDirectory
                    shortcut.iconLocation = os.path.join(assetsDirectory, 'logo_alternate_big.ico')
                    shortcut.save()
                except:
                    try:
                        os.system('python -m pip install pywin32')
                        import win32com.client
                        # Create a shortcut (.lnk) file
                        shortcut_path = os.path.join(shortcut_location, f"{shortcut_name}.lnk")
                        # Create a ShellLink object
                        shell = win32com.client.Dispatch("WScript.Shell")
                        shortcut = shell.CreateShortCut(shortcut_path)
                        # Set the target of the shortcut
                        shortcut.Targetpath = target_file
                        shortcut.WorkingDirectory = frontendDirectory
                        shortcut.iconLocation = os.path.join(assetsDirectory, 'Logo.ico')
                        shortcut.save()
                    except:
                        print('Failed to install dependencies')

            def create_shortcut_mac(target_file, shortcut_location, shortcut_name):
                try:
                    os.system('pip3 intall appscript')
                    import appscript
                    # Create a shortcut (.app) file
                    shortcut_path = os.path.join(shortcut_location, f"{shortcut_name}.app")

                    # Create a new AppleScript script
                    script_content = f'''
                                   tell application "Finder"
                                       make new alias file at folder "{shortcut_location}" to POSIX file "{target_file}"
                                       set name of result to "{shortcut_name}"
                                   end tell
                                   '''

                    # Save the AppleScript to a temporary file
                    script_path = "/tmp/create_shortcut_script.scpt"
                    with open(script_path, 'w') as script_file:
                        script_file.write(script_content)

                    # Run the AppleScript to create the shortcut
                    appscript.run(f"osascript {script_path}")

                    # Remove the temporary AppleScript file
                    os.remove(script_path)
                except:
                    try:
                        os.system('python3 -m pip install appscript')
                        import appscript
                        # Create a shortcut (.app) file
                        shortcut_path = os.path.join(shortcut_location, f"{shortcut_name}.app")

                        # Create a new AppleScript script
                        script_content = f'''
                                       tell application "Finder"
                                           make new alias file at folder "{shortcut_location}" to POSIX file "{target_file}"
                                           set name of result to "{shortcut_name}"
                                       end tell
                                       '''

                        # Save the AppleScript to a temporary file
                        script_path = "/tmp/create_shortcut_script.scpt"
                        with open(script_path, 'w') as script_file:
                            script_file.write(script_content)

                        # Run the AppleScript to create the shortcut
                        appscript.run(f"osascript {script_path}")

                        # Remove the temporary AppleScript file
                        os.remove(script_path)
                    except:
                        try:
                            os.system('python -m pip3 install appscript')
                            import appscript
                        except:
                            print('Failed to install dependencies')

            target_file = os.path.join(frontendDirectory, 'Purrfect_Tube_Downloader.py')
            shortcut_name = "Purrfect Tube Downloader"
            # Create the shortcut
            save_location = askdirectory(title="Choose Save Location")
            if save_location:
                try:
                    create_shortcut_windows(target_file, save_location, shortcut_name)
                    progressLabel.configure(text='Installation Complete')
                    progressLabel.place(relx=0.2)
                    openButton=ctk.CTkButton(root, text='Open', fg_color='red', font=('Cooper Black', 16), hover_color='#cc0000', text_color='white', command=openFile)
                    openButton.place(relx=0.8, rely=0.85, anchor='center')
                except:
                    try:
                        create_shortcut_mac(target_file, save_location, shortcut_name)
                        progressLabel.configure(text='Installation Complete')
                        progressLabel.place(relx=0.2)
                        openButton = ctk.CTkButton(root, text='Open', fg_color='red', font=('Cooper Black', 16),
                                                   hover_color='#cc0000', text_color='white', command=openFile)
                        openButton.place(relx=0.8, rely=0.85, anchor='center')
                    except:
                        print('Failed to create shortcut')
                        progressLabel.configure(text='Installation Complete, Failed to create shortcut \n open the Frontend folder and open manually')
            else:
                progressLabel.configure(text='Installation Complete, Failed to create shortcut \n open the Frontend folder and open manually')
                openButton = ctk.CTkButton(root, text='Open', fg_color='red', font=('Cooper Black', 16),
                                           hover_color='#cc0000', text_color='white', command=openFile)
                openButton.place(relx=0.8, rely=0.85, anchor='center')

    #The big cat
    catPath = os.path.join(assetsDirectory, 'blue_cat.png')
    cat = Photo('blue_cat.png', height=200, width=200)
    cat2 = Photo('blue_cat_blink.png', height=200, width=200)

    titleLabel = ctk.CTkLabel(root, text='Installation Kitten \n Purrfect Tube Downloader', font=('Cooper Black', 20, 'bold'), text_color='red', fg_color='transparent', width=200)
    titleLabel.place(relx=0.5, rely=0.1, anchor='center')

    imageLabel = ctk.CTkLabel(root, image=cat.getImage(), text='', fg_color='transparent')
    imageLabel.place(relx=0.519, rely=0.5, anchor='center')

    installButton=ctk.CTkButton(root, text='Install', fg_color='red', font=('Cooper Black', 16), hover_color='#cc0000', text_color='white', command=install)
    installButton.place(relx=0.5, rely=0.85, anchor='center')

    progressLabel=ctk.CTkLabel(root, text='She helps install the app', fg_color='transparent', text_color='red', font=('Cooper Black', 16))
    progressLabel.place(relx=0.5, rely=0.95, anchor='center')

    def animate():
        import random
        imageLabel.configure(image=cat.getImage())
        if random.randint(0, 10) // 2 == 0:
            imageLabel.configure(image=cat2.getImage())
        root.after(random.randint(50, 1000), animate)
    animate()
    root.mainloop()


except Exception as e:
    print('Sorry, your OS may not be supported')
    print(f'Error: {e}')


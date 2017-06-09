from neovim import attach
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

class Handler:

    def __init__(self):
        self.init_nvim()
        self.init_selenium()
        self.login()
        self.click_resume()
        self.init_variables()
        self.init_mappings()
        self.echo("Web is ready")

    def init_nvim(self):
        """Attach to neovim instance"""
        # TODO: Try, catch
        self.nvim = attach('socket', path='/tmp/nvim')
        self.channel_id = self.nvim.channel_id
        self.echo("Attached to nvim instance. Channel: %d" % self.channel_id)

    def init_selenium(self):
        """Start selenium web driver"""
        # Figure out how firefox can receive window focus
        #self.driver = webdriver.Firefox()
        # TODO: Use explicit waits
        # TODO: Set chrome options
        self.driver = webdriver.Chrome()
        self.driver.get('https://www.codecademy.com/login')

    def login(self):
        """Log into codecademy"""

        email = ""
        password = ""
        # TODO: error handling
        with open("credentials.txt") as credentials:
            email = credentials.readline().rstrip("\n")
            password = credentials.readline().rstrip("\n")

        email_field_name = "user[login]"
        password_field_name = "user[password]"

        email_field = self.driver.find_element_by_name(email_field_name)
        password_field = self.driver.find_element_by_name(password_field_name)

        # Fill login fields
        email_field.send_keys(email)
        password_field.send_keys(password)
        password_field.send_keys(Keys.RETURN)

    def init_variables(self):
        # Editor area
        editor_area_selector = ".editor-container"
        self.editor_area = self.driver.find_element_by_css_selector(editor_area_selector)

        # Run button
        run_button_selector = "._2fDy3KzGIsY8FHMg74ib-V.lx0K4MugD9fFT3l5pAqK1"
        self.run_button = self.driver.find_element_by_css_selector(run_button_selector)

    def click_resume(self):
        """Click resume button at profile page. TODO Use link directly."""
        resume_button_selector = "._2fDy3KzGIsY8FHMg74ib-V._2bwYMUTOYpw6i1TbVOJS4A._1W3U2VJf-f_UqBcW7TFpBs._248uK18apzCUDR-gFWvNIm"
        self.driver.find_element_by_css_selector(resume_button_selector).click()

    def init_mappings(self):
        # Get code from web
        self.nvim.command('nmap <Leader>cg :call rpcnotify(%d, "get")<CR>' % self.channel_id)
        # Send code to web
        self.nvim.command('nmap <Leader>cs :call rpcnotify(%d, "send")<CR>' % self.channel_id)
        # Press run button on web
        self.nvim.command('nmap <Leader>cr :call rpcnotify(%d, "run")<CR>' % self.channel_id)
        # Stop python script
        self.nvim.command('nmap <Leader>st :call rpcnotify(%d, "stop")<CR>' % self.channel_id)
        # TODO mapping to clear input

    def start_loop(self):
        """Start the event loop"""
        self.running = True
        while self.running == True:
            event = self.parse_event()
            self.handle_events(event)

    def parse_event(self):
        raw_event = self.nvim.next_message()
        return raw_event[1]

    def handle_events(self, event):
        """Delegate events to correct handler methods"""
        if event == 'get':
            self.handle_get()
        elif event == 'send':
            self.handle_send()
        elif event == 'run':
            self.handle_run()
        elif event == 'stop':
            self.handle_stop()

    def handle_get(self):
        raw_code = self.editor_area.text
        code = self.remove_line_numbers(raw_code)
        self.enter_code(code)
        
    def enter_code(self, code):
        # TODO: Clear all text first? use 'ggdG'
        # Enter insert mode
        self.nvim.feedkeys("i", "t")
        self.nvim.feedkeys(code, "t")
        # Exit insert mode. TODO: move nvim handling to separate class
        self.nvim.input('<ESC>')

    def remove_line_numbers(self, raw_code):
        """Trims the raw code from the web editor, returning the code without line numbers."""
        trimmed_code = ""
        lines = raw_code.splitlines()
        count = 0
        for line in lines:
            count += 1
            # Every other line contains line the line numbers, dont keep them
            if count % 2 == 0:
                trimmed_code += line + "\n"

        return trimmed_code

    def handle_send(self):
        lines_list = self.nvim.current.buffer.api.get_lines(0,-1,True)
        code = self.lines_list_to_string(lines_list)
        ActionChains(self.driver).click(self.editor_area).send_keys(code).perform()


    def lines_list_to_string(self, lines_list):
        lines = ""
        length = len(lines_list)
        count = 0
        for line in lines_list:
            count += 1
            lines += line
            if count != length:
                lines += "\n"

        return lines
        

    def handle_run(self):
        self.run_button.click()

    def handle_stop(self):
        """Stop the event loop"""
        self.echo('Stopping')
        self.running = False
        self.driver.close()

    def echo(self, msg):
        """Display a message in the attached neovim instance."""
        self.nvim.command('echo "%s"' % msg)

# Start script
Handler().start_loop()

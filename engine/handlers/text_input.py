import pygame as pg
#=====================================#
class TextInput:
    def __init__(self):
        #-------------------------------------#
        self.text = ""
        self.cursor_pos = 0
        #-------------------------------------#
        self.selection_start = None
        self.selection_end = None
        #-------------------------------------#
        self.scroll_offset = 0

    #=====================================#
    def handle_event(self, event):
        #-------------------------------------#
        mods = pg.key.get_mods()
        shift = bool(mods & pg.KMOD_SHIFT)
        ctrl = bool(mods & pg.KMOD_CTRL)
        #-------------------------------------#
        if event.type != pg.KEYDOWN:
            return None
       #=====================================#
        if event.key == pg.K_RETURN:
            text = self.text.strip()
            self.clear()
            return text
        #-------------------------------------#
        # TAB
        elif event.key == pg.K_TAB:
            return "__TAB__"
        #-------------------------------------#
        # BACKSPACE
        elif event.key == pg.K_BACKSPACE:
            #-------------------------------------#
            if self.has_selection():
                self.delete_selection()
            #-------------------------------------#
            elif self.cursor_pos > 0:
                self.text = (
                    self.text[:self.cursor_pos - 1] +
                    self.text[self.cursor_pos:]
                )
                self.cursor_pos -= 1
            #-------------------------------------#
            return "__BACKSPACE__"

        #-------------------------------------#
        # DELETE
        elif event.key == pg.K_DELETE:
            if self.has_selection():
                self.delete_selection()
            else:
                self.text = (
                    self.text[:self.cursor_pos] +
                    self.text[self.cursor_pos + 1:]
                )
            return "__BACKSPACE__"
        #-------------------------------------#
        # LEFT
        elif event.key == pg.K_LEFT:
            if shift:
                if self.selection_start is None:
                    self.selection_start = self.cursor_pos
                self.cursor_pos = max(0, self.cursor_pos - 1)
                self.selection_end = self.cursor_pos
            else:
                self.cursor_pos = max(0, self.cursor_pos - 1)
                self.clear_selection()
        #-------------------------------------#
        # RIGHT
        elif event.key == pg.K_RIGHT:
            #-------------------------------------#
            if shift:
                if self.selection_start is None:
                    self.selection_start = self.cursor_pos
                self.cursor_pos = min(len(self.text), self.cursor_pos + 1)
                self.selection_end = self.cursor_pos
            #-------------------------------------#
            else:
                self.cursor_pos = min(len(self.text), self.cursor_pos + 1)
                self.clear_selection()

        #-------------------------------------#
        # CTRL + x
        elif ctrl and event.key == pg.K_x:
            #-------------------------------------#
            if self.has_selection():
                start, end = sorted([self.selection_start, self.selection_end])
                pg.scrap.put(pg.SCRAP_TEXT, self.text[start:end].encode())
                self.delete_selection()

        #-------------------------------------#
        # CTRL + c
        elif ctrl and event.key == pg.K_c:
            #-------------------------------------#
            if self.has_selection():
                start, end = sorted([self.selection_start, self.selection_end])
                pg.scrap.put(pg.SCRAP_TEXT, self.text[start:end].encode())

        #-------------------------------------#
        # CTRL + v
        elif ctrl and event.key == pg.K_v:
            pasted = pg.scrap.get(pg.SCRAP_TEXT)
            #-------------------------------------#
            if pasted:
                self.insert_text(pasted.decode(errors="ignore").replace("\x00", ""))

        # CTRL + LEFT
        #-------------------------------------#
        elif ctrl and event.key == pg.K_LEFT:
            #-------------------------------------#
            if self.cursor_pos > 0:
                self.cursor_pos -= 1
                while self.cursor_pos > 0 and self.text[self.cursor_pos] == " ":
                    self.cursor_pos -= 1
                while self.cursor_pos > 0 and self.text[self.cursor_pos-1] != " ":
                    self.cursor_pos -= 1

        # CTRL + RIGHT
        #-------------------------------------#
        elif ctrl and event.key == pg.K_RIGHT:
            length = len(self.text)
            while self.cursor_pos < length and self.text[self.cursor_pos] != " ":
                self.cursor_pos += 1
            while self.cursor_pos < length and self.text[self.cursor_pos] == " ":
                self.cursor_pos += 1

        #CTRL + BACKSPACE
        #-------------------------------------#
        elif ctrl and event.key == pg.K_BACKSPACE:
            #-------------------------------------#
            if self.has_selection():
                self.delete_selection()
            #-------------------------------------#
            else:
                start = self.cursor_pos

                while start > 0 and self.text[start-1] == " ":
                    start -= 1
                while start > 0 and self.text[start-1] != " ":
                    start -= 1

                self.text = self.text[:start] + self.text[self.cursor_pos:]
                self.cursor_pos = start

        #-------------------------------------#
        #CTRL + A
        elif ctrl and event.key == pg.K_a:
            if len(self.text) > 0:
                self.selection_start = 0
                self.selection_end = len(self.text)
                self.cursor_pos = len(self.text)
        #-------------------------------------#
        #CTRL + SHIFT
        elif ctrl and shift and event.key == pg.K_LEFT:
            if self.selection_start is None:
                self.selection_start = self.cursor_pos

            old = self.cursor_pos

            # move como ctrl+left
            if self.cursor_pos > 0:
                self.cursor_pos -= 1
                while self.cursor_pos > 0 and self.text[self.cursor_pos] == " ":
                    self.cursor_pos -= 1
                while self.cursor_pos > 0 and self.text[self.cursor_pos-1] != " ":
                    self.cursor_pos -= 1

            self.selection_end = self.cursor_pos

        #-------------------------------------#
        # HOME
        elif event.key == pg.K_HOME:
            self.cursor_pos = 0
            self.clear_selection()
        #-------------------------------------#
        # END
        elif event.key == pg.K_END:
            self.cursor_pos = len(self.text)
            self.clear_selection()
        #-------------------------------------#
        # TEXTO
        elif event.unicode and not ctrl:
            if event.unicode.isprintable():
                self.insert_text(event.unicode)

        #-------------------------------------#
        return None
    
    #------------helpers---------------#
    def set_text(self, text):
        self.text = text
        self.cursor_pos = len(text)
        self.clear_selection()

    def insert_text(self, text):
        if self.has_selection():
            self.delete_selection()

        self.text = (
            self.text[:self.cursor_pos] +
            text +
            self.text[self.cursor_pos:]
        )
        self.cursor_pos += len(text)

    def delete_selection(self):
        start, end = sorted([self.selection_start, self.selection_end])

        self.text = self.text[:start] + self.text[end:]
        self.cursor_pos = start
        self.clear_selection()

    def clear_selection(self):
        self.selection_start = None
        self.selection_end = None

    def has_selection(self):
        return (
            self.selection_start is not None and
            self.selection_end is not None and
            self.selection_start != self.selection_end
        )

    def clear(self):
        self.text = ""
        self.cursor_pos = 0


        self.clear_selection()



        
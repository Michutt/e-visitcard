from images.template_black import template_black
from images.template_red import template_red
from images.ZarazWracam import zarazWracam
from images.plan_black import plan_black
from images.plan_red import plan_red
from fonts import font20, font24

def template(frame_black, frame_red, e):
    e.draw_picture(frame_black, template_black)
    e.draw_picture(frame_red, template_red)

def brb(frame_black, frame_red, e):
    e.draw_small_picture(frame_red, zarazWracam, 13, 400, 38, 272)

def first_screen(frame_black, frame_red, e):
    data = ["dr hab. inz. Grzegorz Lentka", "grzlentk@pg.edu.pl",
     "(58) 347 21 97", "Godziny konsultacji:", "10:00", "14:00"]

    e.display_string_at(frame_black, 100, 100, data[0], font24, 1)
    e.display_string_at(frame_black, 100, 180, data[1], font20, 1)
    e.display_string_at(frame_black, 100, 230, data[2], font20, 1)

    e.display_string_at(frame_black, 500, 250, data[3], font20, 1)
    e.display_string_at(frame_red, 500, 280, data[4], font20, 1)
    e.display_string_at(frame_red, 570, 280, "--", font20, 1)
    e.display_string_at(frame_red, 600, 280, data[5], font20, 1)

def second_screen(frame_black, frame_red, e):
    e.draw_picture(frame_black, plan_black)
    e.draw_picture(frame_red, plan_red)

def third_screen(frame_black, frame_red, e):
    index = 0
    display_word = ""
    data = "Grzegorz Lentka uzyskal tytul magistra inzyniera w roku 1996 na Wydziale Elektroniki, Telekomunikacji i Informatyki Politechniki Gdanskiej w zakresie systemow pomiarowych. Stopien doktora nauk technicznych uzyskal w roku 2003, a doktora habilitowanego w 2014. Obecnie zatrudniony jest w Katedrze Metrologii i Optoelektroniki na stanowisku profesora nadzw. PG"
    data = data.split()

    for word in data:
        if len(display_word) > 48:
            e.display_string_at(frame_black, 30, 80+index*30, display_word, font20, 1)
            display_word = word + " "
            index += 1
        else:
            display_word += word + " " 

    e.display_string_at(frame_black, 30, 80+index*30, display_word, font20, 1)
    e.display_string_at(frame_red, 30, 30, "Notka biograficzna", font24, 1)
    

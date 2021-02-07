from images.template_black import template_black
from images.template_red import template_red
from images.plan_black import plan_black
from images.plan_red import plan_red
from images.kmio import kmio
from images.eti import eti
from fonts import font20, font24
from images.brb import brb
import uos


def template(frame_black, frame_red, e):
    e.draw_picture(frame_black, template_black)
    e.draw_picture(frame_red, template_red)

def be_right_back(frame_black, frame_red, e):
    e.draw_small_picture(frame_red, brb, 100, 400, 38, 272)

def first_screen(frame_black, frame_red, e):
    data = ["dr hab. inz. Grzegorz Lentka", "grzlentk@pg.edu.pl",
     "(58) 347 21 97", "Godziny konsultacji:", "10:00", "--", "14:00"]

    e.display_string_at(frame_black, 100, 100, data[0], font24, 1)
    e.display_string_at(frame_black, 100, 180, data[1], font20, 1)
    e.display_string_at(frame_black, 100, 230, data[2], font20, 1)

    e.display_string_at(frame_black, 500, 250, data[3], font20, 1)
    e.display_string_at(frame_red, 500, 280, data[4], font20, 1)
    e.display_string_at(frame_red, 570, 280, data[5], font20, 1)
    e.display_string_at(frame_red, 600, 280, data[6], font20, 1)

def second_screen(frame_black, frame_red, e):
    e.draw_picture(frame_black, plan_black)
    e.draw_picture(frame_red, plan_red)

def third_screen(frame_black, frame_red, e):
    data = "Grzegorz Lentka uzyskal tytul magistra inzyniera w roku 1996 na Wydziale Elektroniki, Telekomunikacji i Informatyki Politechniki Gdanskiej w zakresie systemow pomiarowych. Stopien doktora nauk technicznych uzyskal w roku 2003, a doktora habilitowanego w 2014. Obecnie zatrudniony jest w Katedrze Metrologii i Optoelektroniki na stanowisku profesora nadzw. PG"
    e.display_text(frame_black, 30, 80, data, font20)
    e.display_string_at(frame_red, 30, 30, "Notka biograficzna", font24, 1)

def fourth_screen(frame_black, frame_red, e):
    e.draw_small_picture(frame_red, kmio, 120, 60, 120, 360)
    e.display_text(frame_black, 40, 210, "Katedra Metrologii i Optoelektroniki prowadzi dwie specjalnosci dydaktyczne:", font20)
    e.display_text(frame_black, 40, 270, "-- Optoelektronika", font20)
    e.display_text(frame_black, 40, 300, "-- Komputerowe Systemy Elektroniczne", font20)
    e.display_text(frame_black, 40, 350, "Dzialajace kola naukowe: ", font20)
    e.display_text(frame_black, 40, 380, "-- Soliton", font20)
    e.display_text(frame_black, 40, 410, "-- PCB", font20)
    e.display_text(frame_black, 40, 440, "-- Biofoton", font20)

def fifth_screen(frame_black, frame_red, e):
    data = "KOMPUTEROWE SYSTEMY ELEKTRONICZNE"
    e.display_text(frame_black, 230, 100, data, font24)
    data = "Specjalnosc dotyczy szerokiej problematyki systemow elektronicznych: pomiarowych, diagnostycznych (w tym ze sztuczna inteligencja), alarmowych, identyfikacja osob i towarow, elektroniki samochodowej, monitorujacych, systemow kontroli jakosci produkcji, elektronizujacych wyroby i innych. Te szeroka klase systemow nazywa sie obecnie infosystemami elektronicznymi."
    e.display_text(frame_black, 30, 200, data, font20)
    e.draw_small_picture(frame_red, eti, 60, 60, 96, 96)

def generated_screen(frame_black, frame_red, e, f_name):
    uos.chdir("images/generated")
    xd = __import__(f_name)
    e.draw_picture(frame_black, getattr(xd, f_name))
    uos.chdir("/flash")

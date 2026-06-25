import configparser

config = configparser.ConfigParser()

config.read('config.ini')


n_times = config.getint('agentes', 'n_times')
n_agentes_p_time = config.getint('agentes', 'n_agentes_p_time')

grid_size = config.getint('mundo', 'grid_size')

panel_width = config.getint('interface', 'panel_width')
tamanho_h_w = config.getint('interface', 'tamanho_height_width')


timer_movimento = config.getint('engine', 'timer_movimento')
fps = config.getint('engine', 'fps_limit')

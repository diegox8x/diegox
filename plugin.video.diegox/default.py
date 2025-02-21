# -*- coding: utf-8 -*-

import sys

if sys.version_info[0] < 3:
    import urllib2
else:
    import urllib.error as urllib2

import os

from configuraciones import config, logger, tools

from dox.item import Item

from configuraciones.config import WebErrorException


logger.info('[COLOR blue]Starting with %s[/COLOR]' % sys.argv[1])

# ~ Obtener parámetros de lo que hay que ejecutar

if sys.argv[2]:
    item = Item().fromurl(sys.argv[2])
else:
    item = Item(channel='mainmenu', action='mainlist')

sys.path.append(os.path.join(config.get_runtime_path(), 'lib'))


# ~ Establecer si channel es un canal web o un módulo

tipo_channel = ''

if item.channel == '' or item.action == '':
    logger.info('Empty channel/action, nothing to do')

else:
    # ~ channel puede ser un canal web o un módulo
    path = os.path.join(config.get_runtime_path(), 'channels', item.channel + ".py")
    if os.path.exists(path):
        tipo_channel = 'channels.'
    else:
        path = os.path.join(config.get_runtime_path(), 'modules', item.channel + ".py")
        if os.path.exists(path):
            tipo_channel = 'modules.'
        else:
            logger.error('Channel/Module not found, nothing to do')


# ~ Ejecutar según los parámetros recibidos

if tipo_channel != '':
    try:
        canal = __import__(tipo_channel + item.channel, fromlist=[''])

        # ~ findvideos se considera reproducible y debe acabar haciendo play (o play_fake en su defecto)
        if item.action == 'findvideos':
            if hasattr(canal, item.action):
                itemlist = canal.findvideos(item)
            else:
                from dox import servertools
                itemlist = servertools.find_video_items(item)

            tools.play_from_itemlist(itemlist, item)

        else:
            # ~ search pide el texto a buscar antes de llamar a la rutina del canal (pasar item.buscando para no mostrar diálogo)
            if item.action == 'search':
                if item.buscando != '':
                    tecleado = item.buscando
                else:
                    last_search = config.get_last_search(item.search_type)

                    search_type = ''

                    if item.search_type == 'all':
                        if item.search_pop:
                            last_search = config.get_setting('search_last_list')
                            search_type = 'para [COLOR yellow]Listas[/COLOR]'

                    elif item.search_type == 'movie':
                        if item.search_video: search_type = 'para [COLOR yellow]Vídeos[/COLOR]'
                        else: search_type = 'para [COLOR yellow]Películas[/COLOR]'

                    elif item.search_type == 'tvshow': search_type = 'para [COLOR yellow]Series[/COLOR]'

                    elif item.search_type == 'documentary': search_type = 'para [COLOR yellow]Documentales[/COLOR]'
                    elif item.search_type == 'person': search_type = 'para [COLOR yellow]Personas[/COLOR]'

                    elif item.search_special == 'torrent': search_type = 'para [COLOR yellow]Torrents[/COLOR]'
                    elif item.search_special == 'anime': search_type = 'para [COLOR yellow]Animes[/COLOR]'
                    elif item.search_special == 'dorama': search_type = 'para [COLOR yellow]Doramas[/COLOR]'

                    tecleado = tools.dialog_input(last_search, 'Texto a buscar ' + search_type)

                if tecleado is not None and tecleado != '':
                    itemlist = canal.search(item, tecleado)

                    if item.buscando == '':
                        search_type = item.search_type

                        if item.search_pop: search_type = 'search_last_list'
                        elif item.search_video: search_type = 'search_last_video'

                        config.set_last_search(search_type, tecleado)
                else:
                    itemlist = []
                    # ~ (desactivar si provoca ERROR: GetDirectory en el log)
                    item.folder = False
                    itemlist = False

            # ~ cualquier otra acción se ejecuta en el canal, y se renderiza si devuelve una lista de items
            else:
                if hasattr(canal, item.action):
                    func = getattr(canal, item.action)
                    itemlist = func(item)
                else:
                    # ~ Si item.folder kodi espera un listado
                    logger.info('Action not found in channel')
                    itemlist = [] if item.folder else False

            if type(itemlist) == list:
                logger.info('renderizar itemlist')
                tools.render_items(itemlist, item)

            elif itemlist == None:
                # ~ Si kodi espera un listado (desactivar si provoca ERROR: GetDirectory en el log)
                logger.info('sin renderizar')
                tools.render_no_items()

            elif itemlist == True:
                logger.info('El canal ha ejecutado correctamente una acción que no devuelve ningún listado.')

            elif itemlist == False:
                logger.info('El canal ha ejecutado una acción que no devuelve ningún listado.')

    except urllib2.URLError as e:
        import traceback
        logger.error(traceback.format_exc())

        # ~ Grab inner and third party errors
        if hasattr(e, 'reason'):
            logger.error("Razon del error, codigo: %s | Razon: %s" % (str(e.reason[0]), str(e.reason[1])))
            texto = "No se puede conectar con el servidor ó con el sitio web"
            tools.dialog_ok(config.__addon_name, texto)

        # ~ Grab server response errors
        elif hasattr(e, 'code'):
            logger.error("Codigo de error HTTP : %d" % e.code)
            tools.dialog_ok(config.__addon_name, "El sitio web no funciona correctamente (error http %d)" % e.code)

    except WebErrorException as e:
        import traceback
        logger.error(traceback.format_exc())

        # ~ Ofrecer buscar en otros canales o en el mismo canal, si está activado en la configuración
        if item.contentType in ['movie', 'tvshow', 'season', 'episode'] and config.get_setting('tracking_weberror_dialog', default=True):
            if item.action == 'findvideos': tools.play_fake()

            item_search = tools.dialogo_busquedas_por_fallo_web(item)
            if item_search is not None:
                tools.itemlist_update(item_search)

        else:
            try: last_ver = updater.check_addon_version()
            except: last_ver = True

            if not last_ver: last_ver = '[I](desfasada)[/I]'
            else: last_ver = ''

            release = '[COLOR goldenrod][B]' + config.get_addon_version().replace('.fix', '-Fix') + str(last_ver) + ' '

            tools.dialog_ok(release + '[COLOR red][B]Error en el canal [COLOR yellow]' + item.channel.capitalize() + '[/B][/COLOR]', 
                                    '[COLOR yellowgreen][B]La web asociada a este canal, parece no estar disponible[/B][/COLOR], puede volver a intentarlo pasados unos minutos, y si el problema persiste compruebe mediante un navegador de internet la web: [COLOR cyan][B]%s[/B][/COLOR]' % (e) )

    except:
        import traceback
        logger.error(traceback.format_exc())

        try: last_ver = updater.check_addon_version()
        except: last_ver = True

        if not last_ver: last_ver = '[I](desfasada)[/I]'
        else: last_ver = ''

        release = '[COLOR goldenrod][B]' + config.get_addon_version().replace('.fix', '-Fix') + str(last_ver) + ' '

        if item.channel in ['mainmenu', 'actions', 'domains', 'downloads', 'favoritos', 'filmaffinitylists', 'filters', 'generos', 'groups', 'helper', 'proxysearch', 'search', 'submnuctext', 'submnuteam', 'tester', 'tmdblists', 'tracking']:
            tools.dialog_ok(release + '[COLOR red][B]Error inesperado en [COLOR gold]' + item.channel.capitalize() + '[/B][/COLOR]',
                                    '[COLOR moccasin][B]Puede estar Corrupto su Fichero de [COLOR chocolate][B]Ajustes[/COLOR][COLOR goldenrod][B] de [/B][/COLOR][COLOR yellow][B]Balandro[/B][/COLOR], Pruebe a [COLOR cyan][B]Re-Instalar el Add-On[/B][/COLOR][COLOR goldenrod][B] (consulte nuestro Telegram ó Foro)[/B][/COLOR][COLOR moccasin][B], ó [/COLOR][COLOR darkcyan][B]bien hay un Error en el Add-On/Modulo.[/B][/COLOR] [COLOR chartreuse][B]Para más detalles, vea el Fichero Log de su Media Center en la Ayuda.[/B][/COLOR]')
        else:
            tools.dialog_ok(release + ' [COLOR red]Error inesperado en [COLOR yellow]' + item.channel.capitalize() + '[/B][/COLOR]',
                                    '[COLOR moccasin][B]Puede deberse a un fallo de Conexión[/B][/COLOR], ó [COLOR cyan][B]la Web asociada al Canal varió su estructura[/B][/COLOR], ó [COLOR goldenrod][B]estar Corrupto su Fichero de [COLOR chocolate][B]Ajustes[/COLOR][COLOR goldenrod][B] de [/B][/COLOR][COLOR yellow][B]Balandro[/B][/COLOR][COLOR moccasin], ó [/COLOR][COLOR darkcyan][B]Hay un Error en el Add-On.[/B][/COLOR] [COLOR chartreuse][B]Para más detalles, vea el Fichero Log de su Media Center en la Ayuda.[/B][/COLOR]')

logger.info('[COLOR blue]Ending with %s[/COLOR]' % sys.argv[1])

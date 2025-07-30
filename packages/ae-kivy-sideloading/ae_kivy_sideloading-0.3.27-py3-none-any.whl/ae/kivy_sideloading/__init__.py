"""
kivy mixin and widgets to integrate a sideloading server in your app
====================================================================

this namespace portion provides widgets and a mixin class for your main app instance to easily integrate and control
the :mod:`ae sideloading server <ae.sideloading_server>` into your :class:`main app <ae.kivy.apps.KivyMainApp>`.


kivy sideloading integration into your main app class
-----------------------------------------------------

add the :class:`SideloadingMainAppMixin` mixin provided by this ae namespace portion to your main app class::

    class MyMainAppClass(SideloadingMainAppMixin, KivyMainApp):

the sub-app of the sideloading server will then automatically be instantiated when your app starts and will initialize
the :attr:`~SideloadingMainAppMixin.sideloading_app` attribute with this sub-app instance.

.. hint::
    if you prefer to instantiate the sideloading server sub-app manually, then specify :class:`SideloadingMainAppMixin`
    after :class:`~ae.kivy.apps.KivyMainApp` in the declaration of your main app class.

adding `sideloading_active` to the `:ref:`app state variables` of your app's :ref:`config files` will ensure that the
running status of the sideloading server gets automatically stored persistent on pause or stop of the app for the next
app start.

the running status of the sideloading server will be restored in the app start event handler method
(:meth:`~SideloadingMainAppMixin.on_app_run`).

to manually start it offering the APK of the embedding app, call the
:meth:`~SideloadingMainAppMixin.on_sideloading_server_start` method passing an empty string and dict::

    self.on_sideloading_server_start("", {})

.. hint:: when you pass the dict with a number in a 'port' key, then it will be used as the server listening port.

if no 'port' gets specified, then :class:`SideloadingMainAppMixin` will calculate an individual port number from the
first character of the :attr:`~ae.core.AppBase.app_name` of the app mixing in this class. this is to prevent
the server socket error `[Errno 98] Address already in use` if two different applications with sideloading are
running on the same device and want to offer sideloading.

to manually pause the sideloading server, call the
:meth:`~SideloadingMainAppMixin.on_sideloading_server_stop` method passing an empty string and dict::

    self.on_sideloading_server_stop("", {})


usage of the sideloading button
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

this ae namespace portion is additionally providing the `SideloadingButton` flow button widget to integrate it in
your Kivy app. This button can be used to:

* start or stop the sideloading server,
* select a file for sideloading via the :class:`~ae.kivy_file_chooser.FileChooserPopup`.
* display file info like the full file path and file length.
* display the URL of your sideloading server as QR code to allow connections from other devices.

to optionally integrate this `SideloadingButton` into your app, add it to the root layout in your app's main kv file
with the `id` `sideloading_button`::

    MyRootLayout:
        ...
        SideloadingButton:
            id: sideloading_button

if the sideloading server is not active and the user is clicking the `SideloadingButton`, then this portion will
first check if the `Downloads` folder of the device is containing an APK file for the running app, and if yes, then the
sideloading server will be started providing the found APK file.

ff the sideloading server is instead already running/active, and the user is tapping on the `SideloadingButton` then a
dropdown menu will be shown with options to (1) display info of the sideloading file, (2) select a new file, (3)
display the sideloading server URL as QR code or (4) stop the sideloading server.


dependencies/requirements in `buildozer.spec`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

to build an Android APK with the kivy sideloading server integrated, make sure that the following external packages
are specified in the `requirements` setting of the `[app]` section of your `buildozer.spec` file.

* ae.kivy_file_chooser
* ae.kivy_iterable_displayer
* ae.kivy_qr_displayer
* ae.kivy_sideloading
* ae.sideloading_server
* kivy_garden.qrcode
* qrcode
* typing_extensions

additionally, the following packages and ae namespace portions required by the above packages have to be included::

        typing_extensions, qrcode, kivy_garden.qrcode,
        ae.base, ae.files, ae.paths, ae.deep, ae.dynamicod, ae.i18n,
        ae.updater, ae.core, ae.literal, ae.console, ae.parse_date, ae.gui,
        ae.kivy_auto_width, ae.kivy_dyn_chi, ae.kivy_relief_canvas, ae.kivy, ae.kivy_user_prefs, ae.kivy_glsl,
        ae.kivy_file_chooser, ae.sideloading_server, ae.kivy_sideloading,
        ae.kivy_iterable_displayer, ae.kivy_qr_displayer


sideloading server life cycle
-----------------------------

to activate the sideloading server to offer a different file, specify the path (or glob file mask) of the file to be
offered/available via sideloading in the :attr:`~SideloadingMainAppMixin.sideloading_file_mask` attribute and then call
the method :meth:`~SideloadingMainAppMixin.on_sideloading_server_start`. this method will check if the specified file
 exists, and if yes, then it will start the sideloading server. if you specify a file mask instead of a concrete
file path, then this method will check if there exists exactly one file matching the file mask.

after the start of the sideloading server, the :attr:`~SideloadingMainAppMixin.sideloading_file_ext` attribute will
contain the file extension of the file available via sideloading.

the sideloading server will automatically be shut down on quit/close of the embedding app. you can alternatively stop
the sideloading server manually at any time by calling the :meth:`~SideloadingMainAppMixin.on_sideloading_server_stop`
method.
"""
import os

from typing import Callable, Optional

from kivy.app import App                                                                    # type: ignore
from kivy.clock import mainthread                                                           # type: ignore
from kivy.lang import Builder                                                               # type: ignore
from kivy.uix.widget import Widget                                                          # type: ignore

from ae.base import UNSET                                                                   # type: ignore
from ae.files import file_transfer_progress                                                 # type: ignore
from ae.i18n import register_package_translations                                           # type: ignore
from ae.sideloading_server import (                                                         # type: ignore
    DEFAULT_APK_FILE_MASK, FILE_COUNT_MISMATCH, server_factory, update_handler_progress, SideloadingServerApp)
from ae.gui.utils import (                                                                  # type: ignore
    APP_STATE_SECTION_NAME, EventKwargsType, id_of_flow, register_package_images)
from ae.gui.app import MainAppBase                                                          # type: ignore
from ae.gui.tours import TourDropdownFromButton                                             # type: ignore
from ae.kivy.widgets import FlowDropDown                                                    # type: ignore
from ae.kivy.i18n import get_txt                                                            # type: ignore

import ae.kivy_file_chooser                                                                 # type: ignore # noqa: F401
import ae.kivy_iterable_displayer                                                           # type: ignore # noqa: F401
import ae.kivy_qr_displayer                                                                 # type: ignore # noqa: F401


__version__ = '0.3.27'


register_package_images()                                                                   # load package images
register_package_translations()                                                             # load package translations
Builder.load_file(os.path.join(os.path.dirname(__file__), "widgets.kv"))                    # declare package widgets


class SideloadingMenuPopup(FlowDropDown):                       # pragma: no cover # pylint: disable=too-many-ancestors
    """ dropdown menu to control sideloading server. """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        main_app = App.get_running_app().main_app
        sideloading_button = main_app.widget_by_id('sideloading_button')
        assert sideloading_button, "missing instance of a sideloading button in the app widgets tree"

        self.child_data_maps = []

        file_path = getattr(main_app.sideloading_app, 'sideloading_file_path')
        if file_path or main_app.debug:
            data = {'mask': main_app.sideloading_file_mask or DEFAULT_APK_FILE_MASK,
                    'extension': main_app.sideloading_file_ext,
                    'path': file_path}
            if file_path:
                try:
                    file_size = os.path.getsize(file_path)
                except (FileNotFoundError, Exception) as ex:        # pylint: disable=broad-exception-caught
                    main_app.vpo(f"{self.__class__.__name__}.__init__({kwargs=}): {ex=} on get size of {file_path=}")
                    file_size = 0
                data['size'] = file_transfer_progress(file_size) + (f" ({file_size} bytes)" if main_app.debug else "")
            self.child_data_maps.append({
                'kwargs': {'text': get_txt("sideloading file info"),
                           'tap_flow_id': id_of_flow('open', 'iterable_displayer', 'sideloading file info'),
                           'tap_kwargs': {'popups_to_close': (self, ), 'popup_kwargs': {
                               'title': os.path.basename(file_path), 'data': data}, 'tap_widget': sideloading_button}}})

        self.child_data_maps.append({
            'kwargs': {'text': get_txt("select file for sideloading"),
                       'tap_flow_id': id_of_flow('open', 'file_chooser', 'sideloading_file_mask'),
                       'tap_kwargs': {'popups_to_close': (self, ),
                                      'popup_kwargs': {'submit_to': 'sideloading_file_mask'},
                                      'tap_widget': sideloading_button}}})

        self.child_data_maps.append({
            'kwargs': {'text': get_txt("display sideloading address/QR code"),
                       'tap_flow_id': id_of_flow('open', 'qr_displayer', 'sideloading_url'),
                       'tap_kwargs': {'popups_to_close': (self, ),
                                      'tap_widget': sideloading_button,
                                      'popup_kwargs': {
                                        'title': main_app.sideloading_app.server_url(),
                                        'qr_content': get_txt("sideloading url")}}}})

        action = 'stop' if main_app.sideloading_active else 'start'
        self.child_data_maps.append({
            'kwargs': {'text': get_txt(action + " sideloading server"),
                       'tap_flow_id': id_of_flow(action, 'sideloading_server'),
                       'tap_kwargs': {'popups_to_close': (self, ), 'tap_widget': sideloading_button}}})


class SideloadingMenuTour(TourDropdownFromButton):                                          # pragma: no cover
    """ user preferences menu tour. """
    def __init__(self, main_app: MainAppBase):
        super().__init__(main_app)
        self.page_ids = [id_of_flow('open', 'sideloading_menu'), TourDropdownFromButton.determine_page_ids]


class SideloadingMainAppMixin:                                                              # pragma: no cover
    """ mixin class with default methods for the main app class. """
    # abstract attributes/properties and methods provided by the main app instance where this gets mixed into
    app_name: str
    change_app_state: Callable
    change_flow: Callable
    dpo: Callable
    framework_root: Widget
    get_opt: Callable
    show_message: Callable
    user_specific_cfg_vars: set
    vpo: Callable

    # implemented attributes
    file_chooser_initial_path: str = ""                 #: used by :mod:`~ae.file_chooser` to select a sideloaded file
    file_chooser_paths: list[str] = []                  #: recently used paths as app state for file chooser

    sideloading_active: tuple = ()                      #: app state flag if the sideloading server is running
    sideloading_app: SideloadingServerApp               #: http sideloading server console app
    sideloading_file_ext: str = "."                     #: extension of the selected sideloading file
    sideloading_file_mask: str = ""                     #: file mask of the sideloading file

    def _init_default_user_cfg_vars(self):
        # noinspection PyProtectedMember,PyUnresolvedReferences
        super()._init_default_user_cfg_vars()
        self.user_specific_cfg_vars |= {                            # pylint: disable=no-member
            (APP_STATE_SECTION_NAME, 'file_chooser_initial_path'),
            (APP_STATE_SECTION_NAME, 'file_chooser_paths'),
            (APP_STATE_SECTION_NAME, 'sideloading_active'),
        }

    def on_app_run(self):
        """ run app event. """
        self.vpo("SideloadingMainAppMixin.on_app_run")

        # instantiate sideloading sub-app and optionally simple http server for apk sideloading
        self.sideloading_app = server_factory(task_id_func=id_of_flow)
        self.sideloading_app.run_app()

        super_method: Optional[Callable] = getattr(super(), 'on_app_run', None)
        if callable(super_method):
            super_method()                      # pylint: disable=not-callable

    def on_app_state_version_upgrade(self, from_version: int):
        """ upgrade app state config vars from the specified app state version to the next one.

        :param from_version:        app state version to upgrade from.
        """
        # super_method: Optional[Callable] = getattr(super(), 'on_app_state_version_upgrade', None)
        super_method = getattr(super(), 'on_app_state_version_upgrade', None)
        if callable(super_method):
            super_method(from_version)          # pylint: disable=not-callable
        self.vpo(f"SideloadingMainAppMixin.on_app_state_version_upgrade {from_version=}")

        if from_version == 3:  # add file chooser and sideloading app state variables
            self.change_app_state('file_chooser_initial_path', "", send_event=False, old_name=UNSET)
            self.change_app_state('file_chooser_paths', [], send_event=False, old_name=UNSET)
            self.change_app_state('sideloading_active', (), send_event=False, old_name=UNSET)

    def on_app_started(self):
        """ initialize and start shaders after kivy app, window and widget root got initialized. """
        super_method: Optional[Callable] = getattr(super(), 'on_app_started', None)
        if callable(super_method):
            super_method()                      # pylint: disable=not-callable

        if self.sideloading_active:
            self.on_sideloading_server_start("", {})

    def on_debug_level_change(self, level_name: str, _event_kwargs: EventKwargsType) -> bool:
        """ debug level app state change flow change confirmation event handler.

        :param level_name:      the new debug level name to be set (passed as flow key).
        :param _event_kwargs:   unused event kwargs.
        :return:                True to confirm the debug level change.
        """
        super_method: Optional[Callable] = getattr(super(), 'on_debug_level_change', None)
        if not callable(super_method) or super_method(level_name, _event_kwargs):   # pylint: disable=not-callable
            self.vpo(f"SideloadingMainAppMixin.on_debug_level_change to {level_name}")
            self.sideloading_app.set_opt('debug_level', self.get_opt('debug_level'))
            return True
        return False

    def on_file_chooser_submit(self, file_path: str, chooser_popup: Widget):
        """ event callback from FileChooserPopup.on_submit() on selection of a file.

        :param file_path:       path string of the selected file.
        :param chooser_popup:   file chooser popup/container widget.
        """
        pre = "SideloadingMainAppMixin.on_file_chooser_submit: "
        self.vpo(f"{pre}file={file_path}; {chooser_popup=}")

        if chooser_popup.submit_to != 'sideloading_file_mask':
            self.dpo(f"{pre}called with submit_to='{chooser_popup.submit_to}'")
            return
        if not os.path.isfile(file_path):
            self.show_message(get_txt("folders can't be send via sideloading"), title=get_txt("select single file"))
            return

        self.sideloading_file_mask = file_path
        if self.sideloading_active:
            self.on_sideloading_server_stop("", {})
        self.on_sideloading_server_start("", {})
        chooser_popup.dismiss()

    def on_sideloading_server_start(self, _flow_key: str, event_kwargs: EventKwargsType) -> bool:
        """ start the sideloading server.

        :param _flow_key:       unused/empty flow key.
        :param event_kwargs:    event kwargs:
                                * 'port': TCP/IP server listening port.
                                * 'tap_widget': button instance that initiated the start of the server.
        :return:                always True to confirm change of flow id.
        """
        @mainthread
        def _upd_pr(client_ip: str = "", transferred_bytes: int = -6, total_bytes: int = 0, **kwargs):
            """ update handler attributes for sideloading_app.client_progress and sideloading progress bars. """
            update_handler_progress(
                client_ip=client_ip, transferred_bytes=transferred_bytes, total_bytes=total_bytes, **kwargs)
            client_ips = list(sap.client_handlers.keys())
            if client_ips and total_bytes:
                fore_last, last = self.sideloading_active
                if client_ip == client_ips[-1]:
                    last = transferred_bytes / total_bytes
                elif len(client_ips) > 1 and client_ip == client_ips[-2]:
                    fore_last = transferred_bytes / total_bytes
                self.change_app_state('sideloading_active', (fore_last, last))

        pre = "SideloadingMainAppMixin.on_sideloading_server_start: "
        self.vpo(f"{pre}{event_kwargs=}")

        if self.sideloading_active:
            self.vpo(f"{pre}stop running sideloading server to restart")
            self.on_sideloading_server_stop("", {})

        sap = self.sideloading_app

        sap.set_opt('port', event_kwargs.get('port', 33300 + ord(self.app_name[0])), save_to_config=False)

        err = sap.start_server(file_mask=self.sideloading_file_mask, progress=_upd_pr, threaded=True)
        if err:
            if FILE_COUNT_MISMATCH in err and 'tap_widget' in event_kwargs:  # let the user select APK if match-count!=1
                # **update_tap_kwargs(event_kwargs['tap_widget'], popup_kwargs={'submit_to': 'sideloading_file_mask'})
                # cannot be used as change_flow-event_kwargs because this would add submit_to key to the sideloading-
                # FlowButton.tap_kwargs which then would have to be removed (ugly) in SideloadingMenuPopup.__init__()
                # after the sideloading-button gets redirected back to open the sideloading-menu.
                self.change_flow(id_of_flow('open', 'file_chooser', 'sideloading_file_mask'),
                                 popup_kwargs={'submit_to': 'sideloading_file_mask',
                                               'opener': event_kwargs['tap_widget']},
                                 tap_widget=event_kwargs['tap_widget'])
            else:
                self.show_message(err, title=get_txt("server start error"))
            return False

        self.sideloading_file_ext = os.path.splitext(sap.sideloading_file_path)[1][1:]
        if event_kwargs:    # only display qr code if called from sideloading_button
            url = sap.server_url()
            self.change_flow(id_of_flow('open', 'qr_displayer', 'sideloading_url'),
                             popup_kwargs={'title': url, 'qr_content': get_txt("sideloading url")})
        self.change_app_state('sideloading_active', (0.0, 0.0))

        return True

    def on_sideloading_server_stop(self, _flow_key: str, _event_kwargs: EventKwargsType) -> bool:
        """ stop a running sideloading http server.

        :param _flow_key:       unused/empty flow key.
        :param _event_kwargs:   unused event kwargs.
        :return:                always True to confirm change of flow id.
        """
        self.vpo("SideloadingMainAppMixin.on_sideloading_server_stop")

        self.sideloading_app.stop_server()
        self.change_app_state('sideloading_active', ())

        return True

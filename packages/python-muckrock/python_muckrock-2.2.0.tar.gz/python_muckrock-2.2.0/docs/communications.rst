Communications
===========

Methods for searching and retrieving FOIA communications. 

CommunicationClient
----------------
.. class:: documentcloud.communications.CommunicationClient

  The communication client allows access to search, list, and retrieve individual FOIA communications. Accessed generally as ``clients.communications`` 
  ::
    >>> comms_list = client.communications.list(foia=14313)
    >>> comms_list
      <APIResults: [<Communication: 108835 - Communication 108835>, <Communication: 108843 - Communication 108843>, <Communication: 108907 - Communication 108907>, <Communication: 108966 - Communication 108966>, <Communication: 111795 - Communication 111795>, <Communication: 116217 - Communication 116217>, <Communication: 117300 - Communication 117300>, <Communication: 125824 - Communication 125824>, <Communication: 126598 - Communication 126598>, <Communication: 132173 - Communication 132173>, <Communication: 132516 - Communication 132516>, <Communication: 137925 - Communication 137925>, <Communication: 138088 - Communication 138088>, <Communication: 145537 - Communication 145537>, <Communication: 152476 - Communication 152476>, <Communication: 152664 - Communication 152664>, <Communication: 160437 - Communication 160437>, <Communication: 160672 - Communication 160672>, <Communication: 168785 - Communication 168785>, <Communication: 169623 - Communication 169623>, <Communication: 178866 - Communication 178866>, <Communication: 179077 - Communication 179077>, <Communication: 191560 - Communication 191560>, <Communication: 201224 - Communication 201224>, <Communication: 209319 - Communication 209319>, <Communication: 210054 - Communication 210054>, <Communication: 217196 - Communication 217196>, <Communication: 217378 - Communication 217378>, <Communication: 224981 - Communication 224981>, <Communication: 225368 - Communication 225368>, <Communication: 232374 - Communication 232374>, <Communication: 232639 - Communication 232639>, <Communication: 240709 - Communication 240709>, <Communication: 240818 - Communication 240818>, <Communication: 249100 - Communication 249100>, <Communication: 250002 - Communication 250002>, <Communication: 257558 - Communication 257558>, <Communication: 258751 - Communication 258751>, <Communication: 266697 - Communication 266697>, <Communication: 267332 - Communication 267332>, <Communication: 277200 - Communication 277200>, <Communication: 277719 - Communication 277719>, <Communication: 285848 - Communication 285848>, <Communication: 285988 - Communication 285988>, <Communication: 294296 - Communication 294296>, <Communication: 294402 - Communication 294402>, <Communication: 304474 - Communication 304474>, <Communication: 304853 - Communication 304853>, <Communication: 314973 - Communication 314973>, <Communication: 315197 - Communication 315197>]>

  .. method:: list(self, **params)

    List all FOIA communications with optional filtering. Available filters include:

    - **max_date**: Filter communications before a specific date. Format: YYYY-MM-DD
    - **min_date**: Filter communications after a specific date. Format: YYYY-MM-DD
    - **foia**: Filter by the associated FOIA request's ID.
    - **status**: Filter by the status of the communication (e.g., `submitted`, `ack`, `processed`, etc.).
    - **response**: Filter communications based on whether they are a response (boolean).

    :param params: Query parameters to filter results (e.g., `foia`, `max_date`, `response`).
    :return: An :class:`APIResults` object containing the list of communications.

  .. method:: retrieve(self, communication_id)

    Retrieve a specific FOIA communication by its unique identifier.

    :param communication_id: The unique ID of the communication to retrieve.
    :return: A :class:`Communication` object representing the requested communication.


Communication
----------------
.. class:: documentcloud.communications.Communication

  A representation of a single FOIA communication.
  
  .. method:: str()

    Returns a string representation of the communication in the format: `Communication {id}`.

  .. method:: get_files(self)

    Retrieve all files associated with this FOIA communication.

    This method fetches any documents or attachments linked to the communication. 
    If no files are associated, it returns an empty :class:`APIResults` object.

    :return: An :class:`APIResults` object containing the list of files.

  .. attribute:: id

    The unique identifier for the communication.

  .. attribute:: foia

    The ID of the associated FOIA request.

  .. attribute:: from_user

    The ID of the user sending this communication.

  .. attribute:: to_user

    The ID of the user receiving this communication.

  .. attribute:: subject

    The subject of the communication, up to 255 characters.

  .. attribute:: datetime

    The date and time when the communication was sent.

  .. attribute:: response

    A boolean indicating if the communication is a response.

  .. attribute:: autogenerated

    A boolean indicating if the communication was autogenerated.

  .. attribute:: communication

    The content or text of the communication.

  .. attribute:: status

    The status of the communication, such as `submitted`, `ack`, `processed`, `done`, etc.

  .. attribute:: files

    A list of integers representing the file IDs associated with this communication.

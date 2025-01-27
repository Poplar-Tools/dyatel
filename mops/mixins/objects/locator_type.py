class LocatorType:
    """
    A container for locator types.

    This class standardizes the locator types used in the Mops framework, ensuring
    consistency and clarity when locating elements within web pages.

    .. note::
        You can specify a locator type along with your locator using the following syntax:

        - :obj:`Element('xpath=//*[@class="class-attribute"]')`
        - :obj:`Element('css=//*[@class="class-attribute"]')`
        - :obj:`Element('text=some text')`
        - :obj:`Element('id=id-without-spaces')`

        The same applies to the :class:`.Locator` object:

        - :obj:`Element(Locator(ios='xpath=//*[@class, "ios-specific"]'))`

    .. note::
        For better readability, you can use this class with the following syntax:

        - :obj:`Element(f'{LocatorType.XPATH}=//*[@class="class-attribute"]')`
    """
    CSS: str = 'css'
    XPATH: str = 'xpath'
    ID: str = 'id'
    TEXT: str = 'text'

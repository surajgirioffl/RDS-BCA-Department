
def getVariablesFromFormat(stringFormat) -> list | None:
    """
        Description:
            Returns a list of variables from a string format.

        Args:
            * stringFormat (str):
                    - Format of a string.

        Returns:
            * list:
                - list of variables extracted from the string format.
            * None:
                - if no variables are found in the format string.
    """
    numberOfBraces = stringFormat.count('{')
    variables = []
    for i in range(numberOfBraces):
        variables.append(
            stringFormat[stringFormat.find('{')+1: stringFormat.find('}')])
        stringFormat = stringFormat[stringFormat.find('}')+1:]
    if variables:
        return variables
    return None


if __name__ == '__main__':
    variables = getVariablesFromFormat('Hello {name}, your age is {age}.')
    print(variables)

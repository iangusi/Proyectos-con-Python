def obtener_operaciones():
    while True:
        cantidad = int(input('Cantidad de operaciones: '))
        print()
        if cantidad <= 5:
            operaciones = [
                validaciones(i)
                for i in range(0,cantidad)
                ]
            return operaciones
        else:
            print('Error: Too many problems.')

def validaciones(i):
    while True:
        operacion = input(f'Ingresa la operación {i+1}: ').replace(' ','')
        simbolo = ''
        contador_simbolos = 0 
        for char in operacion:
            if not char.isdigit():
                simbolo = char
                contador_simbolos += 1
        if contador_simbolos == 1:
            if simbolo == '+' or simbolo == '-':
                num1 = operacion.split(simbolo)[0]
                num2 = operacion.split(simbolo)[1]
                if len(num1) <= 4 or len(num2) <= 4:
                    print('Operación guardada con exito.')
                    print()
                    return {'num1':num1,'num2':num2,'simbolo':simbolo}
                else:
                    print('Error: Numbers cannot be more than four digits.')
            else:
                print("Error: Operator must be '+' or '-'.")
        else:
            print('''Error: The operation was not written properly:
    Numbers must only contain digits.
    There can only be one operation symbol.''')
        print()

def imprimir_y_resolver(operaciones,resolver=False):

    filas = ['   ' for x in range(0,4 if resolver else 3)]

    for operacion in operaciones:

        num1 = operacion['num1']
        num2 = operacion['num2']
        simbolo = operacion['simbolo']
        
        largo_num_mayor = len(num1) if int(num1) > int(num2) else len(num2)

        espacio_entre_operaciones = '    '

        espacio_numero1 = ' '*(largo_num_mayor-len(num1)+2)
        espacio_numero2 = ' '*(largo_num_mayor-len(num2)+1)

        filas[0] += espacio_numero1+num1+espacio_entre_operaciones
        filas[1] += simbolo+espacio_numero2+num2+espacio_entre_operaciones
        filas[2] += ('-'*(largo_num_mayor+2))+espacio_entre_operaciones
        
        if resolver:
            resultado = int(num1)+int(num2) if simbolo == '+' else int(num1)-int(num2)

            espacio_resultado = ' '*(largo_num_mayor+2-len(str(resultado)))
            
            filas[3] += espacio_resultado+str(resultado)+espacio_entre_operaciones

    for fila in filas:
        print(fila)

def main():
    print('Este programa imprime y resuelve sumas y restas entre dos números.')
    print('El máximo de operaciones a ingresar es de 5.')
    print('Como escribir una operación: 32 + 698 ó 32+698')
    print()
    
    operaciones = []
    
    while True:
        print('__MENU__')
        print('1 - Ingresar operaciones')
        print('2 - Imprimir operaciones')
        print('3 - Resolver operaciones')
        print('4 - Salir')
        opc = input('Selecciona una opción: ')
        print()
        if opc == '1':
            operaciones = obtener_operaciones()
        elif opc == '4':
            print('FIN DEL PROGRAMA')
            break
        elif operaciones:
            if opc == '2':
                imprimir_y_resolver(operaciones)
                print()
            elif opc == '3':
                imprimir_y_resolver(operaciones,True)
                print()

main()

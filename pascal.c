#include <stdio.h>

int main() 
{
    int n = 7;          // Número de Linhas
    int matriz[n][n];   // Matriz para armazenar o triângulo
    
    // Passa por cada uma das linhas
    for(int linha = 0; linha < n; linha ++)
    {
        // Passa por cada uma das colunas
        for(int coluna = 0; coluna <= linha; coluna ++) 
        {
            // Verifica se a linha-1 e coluna-1 existem
            // Verifica também se não está na ultima posição da linha
            if(linha - 1 >= 0 && coluna - 1 >= 0 && coluna != linha)
            {
                matriz[linha][coluna] = matriz[linha - 1][coluna] + matriz[linha - 1][coluna - 1];
            } else {
                matriz[linha][coluna]= 1;
            }
            printf("%d ", matriz[linha][coluna]);
        }
        printf("\n");
    }
}

package main

import (
	"flag"
	"fmt"
	"os"
	// "strconv"

	"github.com/ClayCheung/zenbook/pkg/brain"
	_ "github.com/joho/godotenv/autoload"
)

func main() {
	query := flag.String("query", "", "搜索查询(必填)")
	flag.Parse()

	if *query == "" {
		fmt.Println("错误: 必须提供 query 参数")
		flag.Usage()
		os.Exit(1)
	}

	fmt.Printf("您的搜索查询是: %s\n", *query)

	brain := brain.New()

	brain.EntryWithMemory("query", *query)
	brain.Wait()
	answer := brain.GetMemory("answer").(string)
	fmt.Printf("answer:\n%s\n", answer)

	// 定义输出文件路径
	outputPath := "output/answer.md"

	// 创建或打开文件并写入内容
	err := os.MkdirAll("output", os.ModePerm) // 确保目录存在
	if err != nil {
		fmt.Printf("Error creating directory: %v\n", err)
		return
	}

	err = os.WriteFile(outputPath, []byte(answer), 0644)
	if err != nil {
		fmt.Printf("Error writing to file: %v\n", err)
		return
	}

	fmt.Printf("回答已保存到: %s\n", outputPath)

}

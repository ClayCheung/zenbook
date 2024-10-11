package brain

import (
	"fmt"
	"os/exec"

	"github.com/zenmodel/zenmodel/processor"
)

func RunPythonScript(bc processor.BrainContext) error {
	fmt.Println("python script runner assistant running...")

	query := bc.GetMemory("query").(string)

	// exec 执行 python main.py -q "query" -n 9 --json
	cmd := exec.Command("python", "cmd/xhs-scraper.py", "-q", query, "-n", "3", "--json")
	output, err := cmd.Output()
	if err != nil {
		fmt.Printf("err: %v\n", err)
		return err
	}
	fmt.Printf("output: %s\n", string(output))

	bc.SetMemory("result", string(output))
	return nil
}
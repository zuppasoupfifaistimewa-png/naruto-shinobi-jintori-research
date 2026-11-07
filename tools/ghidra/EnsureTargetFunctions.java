import ghidra.app.script.GhidraScript;
import ghidra.program.model.address.Address;
import ghidra.program.model.listing.Function;
import ghidra.program.model.listing.Instruction;

public class EnsureTargetFunctions extends GhidraScript {
    @Override
    protected void run() throws Exception {
        String[] args=getScriptArgs();
        if(args.length==0) throw new IllegalArgumentException("Pass one or more target addresses");
        for(String value:args) {
            long raw=Long.decode(value);
            Address address=toAddr(raw);
            if(!currentProgram.getMemory().contains(address)) {
                println("TARGET_UNMAPPED="+address);
                continue;
            }
            Function function=currentProgram.getFunctionManager().getFunctionAt(address);
            if(function==null) {
                Instruction instruction=currentProgram.getListing().getInstructionAt(address);
                if(instruction==null) {
                    boolean ok=disassemble(address);
                    instruction=currentProgram.getListing().getInstructionAt(address);
                    if(!ok || instruction==null) {
                        println("TARGET_DISASSEMBLY_FAILED="+address);
                        continue;
                    }
                }
                function=createFunction(address, "HA_TARGET_"+Long.toHexString(raw));
            }
            println("TARGET_FUNCTION="+address+"; name="+(function==null?"NONE":function.getName()));
            if(function==null) println("TARGET_FUNCTION_CREATE_FAILED="+address);
        }
    }
}
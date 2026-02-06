/**
 * CampusNexus - Wallet Connect Button Component
 * Premium wallet connection UI with Pera Wallet
 */
import { usePeraWallet } from '../../hooks/usePeraWallet';

export function WalletConnect() {
    const {
        isConnected,
        isConnecting,
        accountAddress,
        error,
        connect,
        disconnect,
        truncateAddress
    } = usePeraWallet();

    const handleClick = () => {
        if (isConnected) {
            disconnect();
        } else {
            connect();
        }
    };

    return (
        <div className="relative">
            <button
                onClick={handleClick}
                disabled={isConnecting}
                className={`
          flex items-center gap-3 px-4 py-2.5 rounded-xl font-semibold
          transition-all duration-300 ease-out
          ${isConnected
                        ? 'bg-gradient-to-r from-emerald-500/20 to-emerald-600/20 border border-emerald-500/50 text-emerald-400 hover:border-emerald-400'
                        : 'bg-gradient-to-r from-indigo-500 to-purple-500 text-white hover:shadow-lg hover:shadow-indigo-500/30 hover:-translate-y-0.5'
                    }
          ${isConnecting ? 'opacity-70 cursor-wait' : 'cursor-pointer'}
        `}
            >
                {/* Wallet Icon */}
                <svg
                    className={`w-5 h-5 ${isConnecting ? 'animate-pulse' : ''}`}
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                >
                    <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        strokeWidth={2}
                        d="M3 10h18M7 15h1m4 0h1m-7 4h12a3 3 0 003-3V8a3 3 0 00-3-3H6a3 3 0 00-3 3v8a3 3 0 003 3z"
                    />
                </svg>

                {/* Button Text */}
                <span>
                    {isConnecting
                        ? 'Connecting...'
                        : isConnected
                            ? truncateAddress()
                            : 'Connect Wallet'
                    }
                </span>

                {/* Connected indicator */}
                {isConnected && (
                    <span className="flex h-2 w-2">
                        <span className="animate-ping absolute inline-flex h-2 w-2 rounded-full bg-emerald-400 opacity-75"></span>
                        <span className="relative inline-flex rounded-full h-2 w-2 bg-emerald-500"></span>
                    </span>
                )}
            </button>

            {/* Error tooltip */}
            {error && (
                <div className="absolute top-full mt-2 left-0 right-0 bg-red-500/20 border border-red-500/50 text-red-400 text-sm px-3 py-2 rounded-lg animate-fade-in">
                    {error}
                </div>
            )}

            {/* Connected address details dropdown */}
            {isConnected && (
                <div className="
          absolute top-full mt-2 right-0 
          bg-slate-800/90 backdrop-blur-xl 
          border border-slate-700 rounded-xl p-3
          opacity-0 invisible group-hover:opacity-100 group-hover:visible
          transition-all duration-200
        ">
                    <p className="text-xs text-slate-400 mb-1">Connected Address</p>
                    <p className="text-sm font-mono text-slate-200">{accountAddress}</p>
                </div>
            )}
        </div>
    );
}

export default WalletConnect;
